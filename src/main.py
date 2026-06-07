import os
import sys
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Query, Request, Depends, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from pydantic import BaseModel, field_validator
from datetime import datetime, timedelta
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from .engine import JyotishEngine
from .translator import generate_coach_insights, get_cosmic_schedule_advice, generate_business_pulse
from .auth.google_auth import GoogleAuthManager
from .auth.apple_auth import AppleAuthManager
from .integrations.gcal import GoogleCalendarManager
from .database.session import init_db, get_db, SessionLocal
from .database.models import User, OAuthCredential, NumerologyProfile
from .database.seed import seed_numerology_profiles_if_empty
from .numerology import NumerologyEngine
from .feedback import FeedbackManager
from .analytics import AnalyticsTracker, AnalyticsDashboard
from .astro_tools import (detect_yogas, check_sade_sati, check_mangal_dosha,
                           calculate_ashtakavarga, calculate_divisional_charts,
                           calculate_varshaphal, calculate_muhurta)
from .timing_advisor import get_timing_advice

from .api.router import router as api_v2_router
from .core.registry import registry
from .services.transits import get_live_transits
from .services.lucky_windows import get_lucky_windows
from .services.alerts import get_subscription_status
from .services.remedies import get_remedies
from .services.personas import identify_persona
from .services.analytics import get_ecosystem_metrics, calculate_unit_economics

app = FastAPI(title="Jyotish Engine Core")
app.include_router(api_v2_router)

@app.get("/health")
async def health():
    return {"status": "ok"}

FALLBACK_EMAIL = "default@psbc.com"

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """Fetch user from cookie, falling back to default."""
    email = request.cookies.get("user_email")
    if email:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            try:
                user = User(email=email)
                db.add(user)
                db.commit()
                db.refresh(user)
            except Exception:
                db.rollback()
                user = db.query(User).filter(User.email == email).first()
        return user
    
    # Return/create default fallback user (Guest)
    user = db.query(User).filter(User.email == FALLBACK_EMAIL).first()
    if not user:
        try:
            user = User(email=FALLBACK_EMAIL)
            db.add(user)
            db.commit()
            db.refresh(user)
        except Exception:
            db.rollback()
            user = db.query(User).filter(User.email == FALLBACK_EMAIL).first()
    return user

# Initialize database on startup
@app.on_event("startup")
def on_startup():
    init_db()
    db = SessionLocal()
    try:
        seed_numerology_profiles_if_empty(db)
    except Exception as e:
        print(f"[seed] Error during profile seeding: {e}")
    finally:
        db.close()
    registry.register("transits", get_live_transits)
    registry.register("lucky_windows", get_lucky_windows)
    registry.register("subscription", get_subscription_status)
    registry.register("remedies", get_remedies)
    registry.register("marketing_persona", identify_persona)


# Initialize engine and auth managers
engine = JyotishEngine()
google_auth = GoogleAuthManager()
apple_auth = AppleAuthManager()
numerology_engine = NumerologyEngine()
feedback_manager = FeedbackManager()
analytics_tracker = AnalyticsTracker()
analytics_dashboard = AnalyticsDashboard()

class BirthDetails(BaseModel):
    date: str  # YYYY-MM-DD
    time: str  # HH:MM
    lat: float
    lon: float
    location_name: str = ""
    timezone_offset: float = 5.5

    @field_validator("date")
    @classmethod
    def validate_date_range(cls, v: str) -> str:
        try:
            year = int(v.split("-")[0])
        except (ValueError, IndexError):
            raise ValueError("date must be YYYY-MM-DD")
        if not (1900 <= year <= 2100):
            raise ValueError("birth year must be between 1900 and 2100")
        return v

    @field_validator("lat")
    @classmethod
    def validate_lat(cls, v: float) -> float:
        if not (-90 <= v <= 90):
            raise ValueError("latitude must be between -90 and 90")
        return v

    @field_validator("lon")
    @classmethod
    def validate_lon(cls, v: float) -> float:
        if not (-180 <= v <= 180):
            raise ValueError("longitude must be between -180 and 180")
        return v

@app.get("/auth/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("user_email")
    return response

# ── Google Auth ──

def _get_redirect_uri(request: Request) -> str:
    """Return redirect URI, preferring env override to avoid 127.0.0.1 vs localhost mismatch."""
    override = os.getenv("REDIRECT_URI")
    if override:
        return override
    uri = str(request.url_for("google_callback"))
    # Normalise to localhost so it matches what is registered in Google Cloud Console
    uri = uri.replace("127.0.0.1", "localhost")
    if not uri.startswith("https") and "localhost" not in uri:
        uri = uri.replace("http", "https")
    return uri

@app.get("/auth/google/login")
async def google_login(request: Request):
    """Initiates Google OAuth Flow."""
    redirect_uri = _get_redirect_uri(request)
    try:
        auth_url, state, code_verifier = google_auth.get_login_url(redirect_uri)
        response = RedirectResponse(auth_url)
        if code_verifier:
            response.set_cookie("_gcv", code_verifier, httponly=True, max_age=600, samesite="lax")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/auth/google/callback")
async def google_callback(request: Request, code: str = None, error: str = None, db: Session = Depends(get_db)):
    """Handles Google OAuth Callback and persists credentials."""
    if error:
        raise HTTPException(status_code=400, detail=f"Google Auth Error: {error}")
    if not code:
        raise HTTPException(status_code=400, detail="No code provided by Google.")

    redirect_uri = _get_redirect_uri(request)

    try:
        code_verifier = request.cookies.get("_gcv")
        creds_dict = google_auth.exchange_code(code, redirect_uri, code_verifier=code_verifier)
        user_email = creds_dict.get("email") or FALLBACK_EMAIL

        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            user = User(email=user_email)
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Persist credentials
        db_creds = db.query(OAuthCredential).filter(OAuthCredential.user_id == user.id).first()
        if not db_creds:
            db_creds = OAuthCredential(user_id=user.id)
            db.add(db_creds)
        
        db_creds.access_token = creds_dict['token']
        db_creds.refresh_token = creds_dict.get('refresh_token')
        db_creds.token_uri = creds_dict['token_uri']
        db_creds.client_id = creds_dict['client_id']
        db_creds.client_secret = creds_dict['client_secret']
        db_creds.scopes = ",".join(creds_dict['scopes'])
        
        db.commit()
        response = RedirectResponse(url="/")
        response.set_cookie(key="user_email", value=user_email, max_age=3600*24*30, httponly=True)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── Apple Auth ──

@app.get("/auth/apple/login")
async def apple_login():
    """Redirects to Apple Login (Mock or direct). In a real app, this might be handled by frontend JS."""
    html_content = """
    <html>
        <body>
            <form id="mock_form" action="/auth/apple/callback" method="POST">
                <input type="hidden" name="id_token" value="mock_apple_pranav@psbc.com">
            </form>
            <script>document.getElementById('mock_form').submit();</script>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/auth/apple/callback")
async def apple_callback(request: Request, id_token: str = Form(...), db: Session = Depends(get_db)):
    """Handles Apple OAuth Callback (POST from Apple)."""
    try:
        payload = apple_auth.verify_id_token(id_token)
        user_email = payload.get("email")
        if not user_email:
            raise HTTPException(status_code=400, detail="Apple ID Token missing email.")

        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            user = User(email=user_email)
            db.add(user)
            db.commit()
            db.refresh(user)
        
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="user_email", value=user_email, max_age=3600*24*30, httponly=True)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/auth/status")
async def auth_status(user: User = Depends(get_current_user)):
    """Checks if the user is authenticated."""
    is_authenticated = user.email != FALLBACK_EMAIL
    has_creds = user.credentials is not None
    return {"authenticated": is_authenticated, "calendar_connected": has_creds, "email": user.email}

@app.post("/api/chart")
async def get_chart(details: BirthDetails, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Detailed POST endpoint for the frontend dashboard with persistence."""
    try:
        # 1. Update/Persist User Profile
        user.location_name = details.location_name
        user.lat = details.lat
        user.lon = details.lon
        user.birth_date = details.date
        user.birth_time = details.time
        user.tz_offset = details.timezone_offset
        db.commit()

        # 2. Standard Astrological Calculation
        local_dt = datetime.strptime(f"{details.date} {details.time}", "%Y-%m-%d %H:%M")
        utc_dt = local_dt - timedelta(hours=details.timezone_offset)
        
        jd = engine.get_julian_day(utc_dt)
        planets = engine.get_planetary_positions(jd)
        houses = engine.get_houses(jd, details.lat, details.lon)
        
        # 3. Daily Transit Calculation
        now_utc = datetime.utcnow()
        now_jd = engine.get_julian_day(now_utc)
        current_planets = engine.get_planetary_positions(now_jd)
        
        # 4. Dasha calculation (needed for personalized directive)
        dashas = engine.get_vimshottari_dashas(planets["Moon"]["longitude"], jd)
        date_now = now_utc.strftime("%Y-%m-%d")
        active_md = next((d for d in dashas if d["start"] <= date_now <= d["end"]), dashas[0])
        active_ad = next((b for b in active_md["bhuktis"] if b["start"] <= date_now <= b["end"]), active_md["bhuktis"][0])

        # 5. Standard Insights (natal chart + today's transit layer + dasha context)
        insights = generate_coach_insights(planets, houses["Lagna"], current_planets,
                                           md_lord=active_md["lord"], ad_lord=active_ad["lord"])

        # 6. Nakshatra (birth Moon nakshatra)
        nakshatra = engine.get_nakshatra(planets["Moon"]["longitude"])

        # 7. Business ROI Pulse
        business_pulse = generate_business_pulse(dashas, now_utc)
        
        # 6. Cosmic OS Intelligence (Persistent Calendar Integration)
        cosmic_schedule = []
        if user:
            db_creds = db.query(OAuthCredential).filter(OAuthCredential.user_id == user.id).first()
            if db_creds:
                try:
                    creds_dict = {
                        'token': db_creds.access_token,
                        'refresh_token': db_creds.refresh_token,
                        'token_uri': db_creds.token_uri,
                        'client_id': db_creds.client_id,
                        'client_secret': db_creds.client_secret,
                        'scopes': db_creds.scopes.split(",")
                    }
                    gcal = GoogleCalendarManager(creds_dict)
                    raw_events = gcal.get_upcoming_events(max_results=5)
                    analyzed_events = [gcal.analyze_event_priority(e) for e in raw_events]
                    cosmic_schedule = get_cosmic_schedule_advice(analyzed_events, current_planets, active_md["lord"])

                    # Persist refreshed token if auto-refresh happened
                    new_token = gcal.get_refreshed_token()
                    if new_token:
                        db_creds.access_token = new_token
                        db.commit()
                except Exception as e:
                    print(f"Calendar Integration Error: {e}")
        
        # 7. Advanced Astrology Calculation Layer
        yogas             = detect_yogas(planets, houses["Lagna"])
        sade_sati         = check_sade_sati(planets["Moon"]["sign"], current_planets["Saturn"]["sign"])
        mangal_dosha      = check_mangal_dosha(planets, houses["Lagna"])
        ashtakavarga      = calculate_ashtakavarga(planets, houses["Lagna"])
        divisional_charts = calculate_divisional_charts(planets, houses["Lagna"])
        varshaphal        = calculate_varshaphal(planets["Sun"]["longitude"], details.lat, details.lon)

        from .translator import HOUSE_MEANINGS, get_varshaphal_impact, get_divisional_impact
        varshaphal["impact"] = get_varshaphal_impact(varshaphal)
        divisional_charts["impact"] = get_divisional_impact(
            divisional_charts.get("d9", {}), divisional_charts.get("d10", {})
        )

        return {
            "jd": jd,
            "ayanamsa": houses["ayanamsa"],
            "lagna": houses["Lagna"],
            "planets": planets,
            "nakshatra": nakshatra,
            "insights": insights,
            "dashas": dashas,
            "business_pulse": business_pulse,
            "cosmic_schedule": cosmic_schedule,
            "yogas": yogas,
            "sade_sati": sade_sati,
            "mangal_dosha": mangal_dosha,
            "ashtakavarga": ashtakavarga,
            "divisional_charts": divisional_charts,
            "varshaphal": varshaphal,
            "house_meanings": HOUSE_MEANINGS
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/quick-decode")
async def quick_decode(date: str, name: str = ""):
    """Provides instant value from just DOB + Name for the landing page hook."""
    try:
        from datetime import datetime
        dt = datetime.strptime(date, "%Y-%m-%d")
        
        # 1. Numerology
        mulank = numerology_engine.calculate_mulank(date)
        bhagyank = numerology_engine.calculate_bhagyank(date)
        
        # 2. Sun Sign (Estimate using noon)
        jd = engine.get_julian_day(dt.replace(hour=12))
        planets = engine.get_planetary_positions(jd)
        sun_sign = planets.get("Sun", {}).get("sign", "Aries")
        
        # 3. Get Insights
        from .translator import SIGN_NATAL, SIGN_THEMES
        theme = SIGN_THEMES.get(sun_sign, {}).get("theme", "Intelligence")
        natal = SIGN_NATAL.get(sun_sign, "You carry a unique cosmic signature.")
        
        return {
            "mulank": mulank,
            "bhagyank": bhagyank,
            "sun_sign": sun_sign,
            "theme": theme,
            "natal": natal,
            "quote": f"You carry the energy of {sun_sign}. {natal}"
        }
    except Exception as e:
        print(f"Quick decode error: {e}")
        return {"error": str(e)}

@app.get("/api/sky/today")
async def sky_today():
    """Returns today's live sky state for the landing page — no user input required."""
    try:
        from datetime import datetime, timezone as tz
        now = datetime.now(tz.utc)
        jd = engine.get_julian_day(now)
        planets = engine.get_planetary_positions(jd)

        sun_lon  = planets.get("Sun",  {}).get("longitude", 0)
        moon_lon = planets.get("Moon", {}).get("longitude", 0)

        tithi_idx = int(((moon_lon - sun_lon + 360) % 360) / 12)
        yoga_idx  = int(((sun_lon + moon_lon) % 360) / (360 / 27))
        paksha    = "Shukla" if tithi_idx < 15 else "Krishna"

        TITHI = ["Pratipada","Dvitiya","Tritiya","Chaturthi","Panchami","Shashthi","Saptami",
                 "Ashtami","Navami","Dashami","Ekadashi","Dvadashi","Trayodashi","Chaturdashi","Purnima",
                 "Pratipada","Dvitiya","Tritiya","Chaturthi","Panchami","Shashthi","Saptami",
                 "Ashtami","Navami","Dashami","Ekadashi","Dvadashi","Trayodashi","Chaturdashi","Amavasya"]
        YOGA  = ["Vishkambha","Preeti","Ayushman","Saubhagya","Shobhana","Atiganda","Sukarma",
                 "Dhriti","Shoola","Ganda","Vriddhi","Dhruva","Vyaghata","Harshana","Vajra",
                 "Siddhi","Vyatipata","Variyana","Parigha","Shiva","Siddha","Sadhya","Shubha",
                 "Shukla","Brahma","Indra","Vaidhriti"]

        retro = [n for n, d in planets.items() if d.get("is_retrograde") and n not in ("Rahu", "Ketu")]

        return {
            "moon_sign": planets["Moon"]["sign"],
            "moon_deg":  round(planets["Moon"]["degree_in_sign"], 1),
            "sun_sign":  planets["Sun"]["sign"],
            "tithi":     TITHI[tithi_idx],
            "paksha":    paksha,
            "yoga":      YOGA[yoga_idx % 27],
            "retrograde": retro,
            "date":      now.strftime("%d %b %Y"),
        }
    except Exception as e:
        print(f"Sky today error: {e}")
        return {"error": str(e)}

@app.get("/api/user/profile")
async def get_profile(user: User = Depends(get_current_user)):
    """Fetches the persistent user profile."""
    if user.email == FALLBACK_EMAIL or not user.birth_date:
        return {"status": "empty", "new_user": True, "email": user.email}
    
    return {
        "status": "success",
        "date": user.birth_date,
        "time": user.birth_time,
        "lat": user.lat,
        "lon": user.lon,
        "location_name": user.location_name,
        "offset": user.tz_offset
    }


class NumerologyRequest(BaseModel):
    birth_date: str  # YYYY-MM-DD
    full_name: str

class JyotishNumerologyRequest(BaseModel):
    birth_date: str  # YYYY-MM-DD
    full_name: str
    gender: str = "Male"

class FeedbackRequest(BaseModel):
    rating: int  # 1-5
    feedback_text: str
    feature_used: str = ""
    session_id: str = "anonymous"

@app.post("/api/numerology/jyotish")
async def get_jyotish_numerology(request: JyotishNumerologyRequest):
    """Calculate Jyotish numerology profile from user's own birth details."""
    try:
        dt = datetime.strptime(request.birth_date, "%Y-%m-%d")
        dob_formatted = dt.strftime("%d-%m-%Y")
        parts = request.full_name.strip().split()
        first = parts[0] if parts else ""
        last = parts[-1] if len(parts) > 1 else ""
        middle = " ".join(parts[1:-1]) if len(parts) > 2 else ""
        result = numerology_engine.get_jyotish_profile(
            dob=dob_formatted,
            first_name=first,
            middle_name=middle,
            last_name=last,
            gender=request.gender
        )
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/numerology")
async def get_numerology(request: NumerologyRequest):
    """Calculate complete numerology reading."""
    try:
        result = numerology_engine.get_complete_numerology(
            request.birth_date,
            request.full_name
        )
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/feedback")
async def submit_feedback(request: Request, feedback: FeedbackRequest, db: Session = Depends(get_db)):
    """Submit user feedback with auto-categorization."""
    try:
        # Get client information
        user_agent = request.headers.get("user-agent", "")
        client_ip = request.client.host if request.client else ""
        
        feedback_data = {
            "rating": feedback.rating,
            "feedback_text": feedback.feedback_text,
            "feature_used": feedback.feature_used,
            "session_id": feedback.session_id,
            "user_id": None  # For now, anonymous feedback
        }
        
        result = feedback_manager.submit_feedback(db, feedback_data, user_agent, client_ip)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["message"])
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/feedback/stats")
async def get_feedback_stats(days: int = Query(30, ge=1, le=365), db: Session = Depends(get_db)):
    """Get feedback statistics for dashboard."""
    try:
        return feedback_manager.get_feedback_stats(db, days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/feedback/recent")
async def get_recent_feedback(limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    """Get recent feedback entries for review."""
    try:
        return feedback_manager.get_recent_feedback(db, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analytics/track")
async def track_event(request: Request, event_data: Dict[str, Any], db: Session = Depends(get_db)):
    """Track user events and page views."""
    try:
        user_agent = request.headers.get("user-agent", "")
        client_ip = request.client.host if request.client else ""
        
        event_type = event_data.get("event_type", "unknown")
        
        if event_type == "page_view":
            result = analytics_tracker.track_page_view(
                page=event_data.get("page", "/"),
                user_agent=user_agent,
                ip_address=client_ip,
                session_id=event_data.get("session_id", "anonymous"),
                referrer=event_data.get("referrer", "")
            )
        elif event_type == "feature_usage":
            result = analytics_tracker.track_feature_usage(
                feature=event_data.get("feature", "unknown"),
                user_id=event_data.get("user_id"),
                session_id=event_data.get("session_id", "anonymous"),
                metadata=event_data.get("metadata", {})
            )
        elif event_type == "conversion":
            result = analytics_tracker.track_conversion(
                conversion_type=event_data.get("conversion_type", "unknown"),
                value=event_data.get("value", 0),
                user_id=event_data.get("user_id"),
                session_id=event_data.get("session_id", "anonymous")
            )
        else:
            result = {"error": f"Unknown event type: {event_type}"}
        
        return {"success": True, "tracked": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/numerology/profiles")
async def list_numerology_profiles(db: Session = Depends(get_db)):
    """List all people in the numerology profile directory."""
    profiles = db.query(NumerologyProfile).order_by(NumerologyProfile.label).all()
    return [
        {
            "label": p.label,
            "name": " ".join(filter(None, [p.first_name, p.middle_name, p.last_name])),
            "gender": p.gender,
            "dob": p.dob,
        }
        for p in profiles
    ]

@app.get("/api/numerology/profile/{label}")
async def get_numerology_profile(label: str, db: Session = Depends(get_db)):
    """Get full Jyotish numerology profile for a person by their label."""
    profile = db.query(NumerologyProfile).filter(NumerologyProfile.label == label).first()
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile '{label}' not found")
    jyotish = numerology_engine.get_jyotish_profile(
        dob=profile.dob,
        first_name=profile.first_name or "",
        middle_name=profile.middle_name or "",
        last_name=profile.last_name or "",
        gender=profile.gender or "Male",
    )
    return {
        "label": profile.label,
        "name": " ".join(filter(None, [profile.first_name, profile.middle_name, profile.last_name])),
        "gender": profile.gender,
        "dob": profile.dob,
        **jyotish,
    }

@app.get("/api/analytics/summary")
async def get_analytics_summary(days: int = Query(30, ge=1, le=365), db: Session = Depends(get_db)):
    """Get analytics summary dashboard."""
    try:
        return analytics_dashboard.get_analytics_summary(db, days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/numerology/cycles")
async def get_personal_cycles(birth_date: str = Query(..., description="YYYY-MM-DD")):
    """Personal Year, Month, and Day cycle numbers based on Bhagyank."""
    try:
        dt = datetime.strptime(birth_date, "%Y-%m-%d")
        dob_formatted = dt.strftime("%d-%m-%Y")
        today_ist = datetime.utcnow() + timedelta(hours=5, minutes=30)
        result = numerology_engine.get_personal_cycles(dob_formatted, today_ist)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/numerology/compatibility")
async def get_compatibility(label_a: str, label_b: str, db: Session = Depends(get_db)):
    """Compare two people from the NumerologyProfile directory."""
    pa = db.query(NumerologyProfile).filter(NumerologyProfile.label == label_a).first()
    pb = db.query(NumerologyProfile).filter(NumerologyProfile.label == label_b).first()
    if not pa:
        raise HTTPException(status_code=404, detail=f"Profile '{label_a}' not found")
    if not pb:
        raise HTTPException(status_code=404, detail=f"Profile '{label_b}' not found")

    profile_a = numerology_engine.get_jyotish_profile(
        dob=pa.dob, first_name=pa.first_name or "", middle_name=pa.middle_name or "",
        last_name=pa.last_name or "", gender=pa.gender or "Male"
    )
    profile_b = numerology_engine.get_jyotish_profile(
        dob=pb.dob, first_name=pb.first_name or "", middle_name=pb.middle_name or "",
        last_name=pb.last_name or "", gender=pb.gender or "Male"
    )
    compat = numerology_engine.get_two_person_compatibility(profile_a, profile_b)
    return {
        "person_a": {"label": label_a, "name": " ".join(filter(None, [pa.first_name, pa.middle_name, pa.last_name])), **profile_a},
        "person_b": {"label": label_b, "name": " ".join(filter(None, [pb.first_name, pb.middle_name, pb.last_name])), **profile_b},
        "compatibility": compat,
    }


class CompatibilityV2Request(BaseModel):
    name_a: str
    dob_a: str
    gender_a: str
    name_b: str = None
    dob_b: str = None
    gender_b: str = "Male"
    label_b: str = None


@app.post("/api/numerology/compatibility/v2")
async def get_compatibility_v2(req: CompatibilityV2Request, db: Session = Depends(get_db)):
    """Modern compatibility endpoint supporting custom input and atlas profiles."""
    try:
        # Person A (Always custom/user)
        # Engines expect DD-MM-YYYY
        dob_a_fmt = datetime.strptime(req.dob_a, "%Y-%m-%d").strftime("%d-%m-%Y")
        profile_a = numerology_engine.get_jyotish_profile(
            dob=dob_a_fmt, first_name=req.name_a, middle_name="", last_name="", gender=req.gender_a
        )

        # Person B (Custom or Atlas)
        if req.label_b:
            pb = db.query(NumerologyProfile).filter(NumerologyProfile.label == req.label_b).first()
            if not pb:
                raise HTTPException(status_code=404, detail="Atlas profile not found")
            profile_b = numerology_engine.get_jyotish_profile(
                dob=pb.dob, first_name=pb.first_name, middle_name=pb.middle_name or "",
                last_name=pb.last_name or "", gender=pb.gender or "Male"
            )
            name_b = f"{pb.first_name} {pb.last_name or ''}".strip()
        else:
            if not req.dob_b:
                raise HTTPException(status_code=400, detail="Missing birth details for Person 2")
            dob_b_fmt = datetime.strptime(req.dob_b, "%Y-%m-%d").strftime("%d-%m-%Y")
            profile_b = numerology_engine.get_jyotish_profile(
                dob=dob_b_fmt, first_name=req.name_b, middle_name="", last_name="", gender=req.gender_b
            )
            name_b = req.name_b

        comp = numerology_engine.get_two_person_compatibility(profile_a, profile_b)
        
        # Add a friendly interpretation
        interpretation = f"You both share a unique energetic bond. {comp['verdict']} suggests that when you work together, your combined strength is amplified."
        if comp['score'] >= 75:
            interpretation = "This is a Power Match. Your energies are naturally in sync, making this combination excellent for both business and personal growth."
        elif comp['score'] < 50:
            interpretation = "This combination carries some dynamic tension. While it might feel challenging, it often leads to the most growth if you communicate clearly."

        return {
            "person_a": {
                "name": req.name_a, 
                "mulank": profile_a["mulank"], 
                "bhagyank": profile_a["bhagyank"],
                "driver_planet": profile_a["number_meanings"][profile_a["mulank"]]["planet"],
                "conductor_planet": profile_a["number_meanings"][profile_a["bhagyank"]]["planet"]
            },
            "person_b": {
                "name": name_b, 
                "mulank": profile_b["mulank"], 
                "bhagyank": profile_b["bhagyank"],
                "driver_planet": profile_b["number_meanings"][profile_b["mulank"]]["planet"],
                "conductor_planet": profile_b["number_meanings"][profile_b["bhagyank"]]["planet"]
            },
            "compatibility": comp,
            "interpretation": interpretation
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/timing/advisor")
async def timing_advisor(user: User = Depends(get_current_user)):
    """Business timing advice based on stored user profile."""
    if not user.birth_date:
        raise HTTPException(status_code=400, detail="No saved chart. Generate your chart first.")
    try:
        local_dt = datetime.strptime(f"{user.birth_date} {user.birth_time}", "%Y-%m-%d %H:%M")
        utc_dt = local_dt - timedelta(hours=user.tz_offset or 5.5)
        jd = engine.get_julian_day(utc_dt)
        planets = engine.get_planetary_positions(jd)
        now_jd = engine.get_julian_day(datetime.utcnow())
        current_planets = engine.get_planetary_positions(now_jd)
        dashas = engine.get_vimshottari_dashas(planets["Moon"]["longitude"], jd)
        nakshatra = engine.get_nakshatra(planets["Moon"]["longitude"])

        lat = user.lat if user.lat is not None else 28.6139
        lon = user.lon if user.lon is not None else 77.2090
        natal_houses = engine.get_houses(jd, lat, lon)
        lagna_sign = natal_houses["Lagna"]["sign"]

        from .astro_tools import _house
        planet_house = {}
        for p, info in current_planets.items():
            if "sign" in info:
                planet_house[p] = _house(info["sign"], lagna_sign)

        from .translator import generate_business_pulse
        pulse = generate_business_pulse(dashas, datetime.utcnow())
        active_dasha = pulse.get("active_dasha", "Sun-Sun")

        dob_fmt = datetime.strptime(user.birth_date, "%Y-%m-%d").strftime("%d-%m-%Y")
        today_ist_ta = datetime.utcnow() + timedelta(hours=5, minutes=30)
        cycles_ta = numerology_engine.get_personal_cycles(dob_fmt, today_ist_ta)
        advice = get_timing_advice(
            active_dasha, current_planets, nakshatra.get("name", ""),
            personal_day=cycles_ta["personal_day"]["number"],
            planet_house=planet_house
        )
        return advice
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/brief/morning")
async def morning_brief(user: User = Depends(get_current_user)):
    """Daily morning brief: personal day number + transit highlights + timing window."""
    if not user.birth_date:
        raise HTTPException(status_code=400, detail="No saved chart. Generate your chart first.")
    try:
        local_dt = datetime.strptime(f"{user.birth_date} {user.birth_time}", "%Y-%m-%d %H:%M")
        utc_dt = local_dt - timedelta(hours=user.tz_offset or 5.5)
        jd = engine.get_julian_day(utc_dt)
        planets = engine.get_planetary_positions(jd)
        now_jd = engine.get_julian_day(datetime.utcnow())
        current_planets = engine.get_planetary_positions(now_jd)
        dashas = engine.get_vimshottari_dashas(planets["Moon"]["longitude"], jd)
        nakshatra = engine.get_nakshatra(planets["Moon"]["longitude"])

        lat = user.lat if user.lat is not None else 28.6139
        lon = user.lon if user.lon is not None else 77.2090
        natal_houses = engine.get_houses(jd, lat, lon)
        lagna_sign = natal_houses["Lagna"]["sign"]

        from .astro_tools import _house
        planet_house = {}
        for p, info in current_planets.items():
            if "sign" in info:
                planet_house[p] = _house(info["sign"], lagna_sign)

        from .translator import generate_business_pulse
        pulse = generate_business_pulse(dashas, datetime.utcnow())
        active_dasha = pulse.get("active_dasha", "Sun-Sun")

        dob_formatted = datetime.strptime(user.birth_date, "%Y-%m-%d").strftime("%d-%m-%Y")
        today_ist = datetime.utcnow() + timedelta(hours=5, minutes=30)
        cycles = numerology_engine.get_personal_cycles(dob_formatted, today_ist)

        timing = get_timing_advice(
            active_dasha, current_planets, nakshatra.get("nakshatra", ""),
            personal_day=cycles["personal_day"]["number"],
            planet_house=planet_house
        )
        top_action = timing["actions"][0] if timing["actions"] else {}

        # Transit highlights: check if any planet is in a sign that matches natal key planets
        highlights = []
        natal_moon_sign = planets["Moon"]["sign"]
        if current_planets.get("Jupiter", {}).get("sign") == natal_moon_sign:
            highlights.append("Jupiter transiting your natal Moon sign — expanded emotional wisdom, good for decisions.")
        if current_planets.get("Saturn", {}).get("sign") == natal_moon_sign:
            highlights.append("Saturn on natal Moon — discipline required, avoid emotional reactivity.")
        if current_planets.get("Rahu", {}).get("sign") == planets["Sun"]["sign"]:
            highlights.append("Rahu conjunct natal Sun — ambition amplified, stay grounded.")
        moon_sign_now = current_planets.get("Moon", {}).get("sign", "")
        if moon_sign_now:
            highlights.append(f"Moon transiting {moon_sign_now} today.")

        return {
            "date": today_ist.strftime("%Y-%m-%d"),
            "day_name": today_ist.strftime("%A"),
            "personal_day":   cycles["personal_day"],
            "personal_month": cycles["personal_month"],
            "personal_year":  cycles["personal_year"],
            "active_dasha": active_dasha,
            "overall_window": timing["overall_window"],
            "overall_description": timing["overall_description"],
            "top_action": top_action,
            "transit_highlights": highlights,
            "nakshatra": nakshatra.get("name", ""),
            "best_day_this_week": timing["best_day_this_week"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/numerology/forecast")
async def get_yearly_forecast(
    birth_date: str = Query(..., description="YYYY-MM-DD"),
    year: int = Query(None, description="Forecast year (defaults to current year)"),
):
    """12-month Personal Year forecast based on Bhagyank."""
    try:
        from datetime import timezone
        dt = datetime.strptime(birth_date, "%Y-%m-%d")
        dob_formatted = dt.strftime("%d-%m-%Y")
        if year is None:
            year = (datetime.utcnow() + timedelta(hours=5, minutes=30)).year
        return numerology_engine.get_yearly_forecast(dob_formatted, year)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/forecast/yearly")
async def get_yearly_forecast_full(
    year: int = Query(None, description="Forecast year (defaults to current IST year)"),
    user: User = Depends(get_current_user),
):
    """Yearly forecast combining numerology Personal Year with month-by-month Dasha overlay."""
    if not user.birth_date:
        raise HTTPException(status_code=400, detail="No saved chart. Generate your chart first.")
    try:
        if year is None:
            year = (datetime.utcnow() + timedelta(hours=5, minutes=30)).year

        dob_formatted = datetime.strptime(user.birth_date, "%Y-%m-%d").strftime("%d-%m-%Y")
        forecast = numerology_engine.get_yearly_forecast(dob_formatted, year)

        # Dasha overlay — compute active MD/AD lord for the 15th of each month
        local_dt = datetime.strptime(f"{user.birth_date} {user.birth_time}", "%Y-%m-%d %H:%M")
        utc_dt = local_dt - timedelta(hours=user.tz_offset or 5.5)
        jd = engine.get_julian_day(utc_dt)
        planets = engine.get_planetary_positions(jd)
        dashas = engine.get_vimshottari_dashas(planets["Moon"]["longitude"], jd)

        dasha_overlay = []
        for m in forecast["months"]:
            probe = datetime(year, m["month"], 15).strftime("%Y-%m-%d")
            active_md = next((d for d in dashas if d["start"] <= probe <= d["end"]), dashas[0])
            active_ad = next((b for b in active_md["bhuktis"] if b["start"] <= probe <= b["end"]), active_md["bhuktis"][0])
            dasha_overlay.append({
                "month": m["month"],
                "md_lord": active_md["lord"],
                "ad_lord": active_ad["lord"],
                "ad_end": active_ad["end"],
            })

        forecast["dasha_overlay"] = dasha_overlay
        return forecast
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/chart/muhurta")
async def get_muhurta(days: int = Query(7, ge=1, le=30)):
    """Return auspicious windows for the next N days (IST)."""
    try:
        windows = calculate_muhurta(days)
        return {"muhurta_windows": windows, "days_ahead": days}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi.responses import FileResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404 and "text/html" in request.headers.get("accept", ""):
        return FileResponse("src/static/index.html")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

# ── Hindi Translation Endpoint (Gemini 1.5 Flash — POWER zone) ──
class TranslateRequest(BaseModel):
    texts: List[str]
    target: str = "hi"

@app.post("/api/translate")
async def translate_texts(req: TranslateRequest):
    """Batch-translate UI strings to Hindi via Gemini 1.5 Flash."""
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        raise HTTPException(status_code=503, detail="GEMINI_API_KEY not configured")
    if not req.texts:
        return {"translations": []}

    try:
        from google import genai as gai
        client = gai.Client(api_key=api_key)

        numbered = "\n".join(f"{i+1}. {t}" for i, t in enumerate(req.texts))
        prompt = (
            "Translate the following English strings to natural, conversational Hindi. "
            "Keep astrology and numerology Sanskrit terms exactly as-is "
            "(Dasha, Bhukti, Nakshatra, Lagna, Yoga, Tithi, Muhurta, Mulank, Bhagyank, "
            "KUA, Ashtakavarga, Navamsa, Dasamsa, Varshaphal, Sade Sati, Mangal Dosha). "
            "Return ONLY the translated lines in the same numbered format. No extra text.\n\n"
            + numbered
        )

        import time
        max_retries = 3
        backoff = 2
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=prompt
                )
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                time.sleep(backoff)
                backoff *= 2

        raw = response.text.strip()

        # Parse numbered lines back into list
        translations = []
        for line in raw.split("\n"):
            line = line.strip()
            if not line:
                continue
            # Strip leading "N. " pattern
            import re
            cleaned = re.sub(r"^\d+\.\s*", "", line)
            translations.append(cleaned)

        # Pad or trim to match input length
        while len(translations) < len(req.texts):
            translations.append(req.texts[len(translations)])
        translations = translations[:len(req.texts)]

        return {"translations": translations}

    except Exception as e:
        # Graceful fallback to prevent 500 errors during Gemini rate limits
        print(f"Gemini Translation rate limit / error, using local fallback: {e}")
        fallback_trans = {
            "today's energy": "आज की ऊर्जा",
            "core identity": "मूल पहचान",
            "life timing": "जीवन का समय",
            "today": "आज",
            "this week": "इस सप्ताह",
            "numbers": "अंक",
            "full chart": "पूर्ण चार्ट"
        }
        translations = []
        for t in req.texts:
            key = t.strip().lower()
            translations.append(fallback_trans.get(key, t))
        return {"translations": translations}

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_coach(req: ChatRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Conversational Sanctuary Chatbot with voice input and token tracking."""
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        raise HTTPException(status_code=503, detail="GEMINI_API_KEY not configured")
    if not req.message:
        raise HTTPException(status_code=400, detail="Empty message")

    if not user.birth_date:
        return {
            "response": "Greetings. I am your Cosmic OS executive strategic coach. To begin our session, please enter your birth details in the dashboard first. This allows me to analyze your precise sidereal chart, active Vimshottari Dasha cycles, and numerology atlas for personalized counsel.",
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        }

    try:
        from datetime import datetime, timedelta
        local_dt = datetime.strptime(f"{user.birth_date} {user.birth_time}", "%Y-%m-%d %H:%M")
        utc_dt = local_dt - timedelta(hours=user.tz_offset)
        jd = engine.get_julian_day(utc_dt)
        planets = engine.get_planetary_positions(jd)
        houses = engine.get_houses(jd, user.lat, user.lon)

        dashas = engine.get_vimshottari_dashas(planets["Moon"]["longitude"], jd)
        now_utc = datetime.utcnow()
        date_now = now_utc.strftime("%Y-%m-%d")
        active_md = next((d for d in dashas if d["start"] <= date_now <= d["end"]), dashas[0])
        active_ad = next((b for b in active_md["bhuktis"] if b["start"] <= date_now <= b["end"]), active_md["bhuktis"][0])

        now_jd = engine.get_julian_day(now_utc)
        current_planets = engine.get_planetary_positions(now_jd)

        lagna_sign = houses["Lagna"]["sign"]
        placements = []
        from .translator import get_house
        for pname in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"):
            if pname in planets:
                ps = planets[pname]["sign"]
                ph = get_house(ps, lagna_sign)
                placements.append(f"{pname} in {ps} ({ph}H)")
        natal_placements_summary = ", ".join(placements)

        try:
            num_res = numerology_engine.get_complete_numerology(user.birth_date, user.full_name or "Pranav Singhal")
        except Exception:
            num_res = {}

        system_prompt = (
            "You are the Cosmic OS Personal Life & Executive Coach (PSBC Premium Sanctuary).\n"
            f"You are conducting a private strategic session with the user {user.full_name or 'Pranav Singhal'}.\n"
            "Speak in a deeply empathetic, warm, soulful, yet highly clear and practical life-strategist voice. Your goal is to reduce their stress, guide their decision-making, and offer simple, actionable solutions for their day-to-day life.\n"
            "ABSOLUTELY BAN all dry, cold, mechanical, or overly technical jargon (e.g. do not say 'systemic debt', 'operational battery-leakage', 'capital-retention friction', 'speculative-entropy', or 'alignment-gap'). Focus instead on human experiences, feelings, and clear daily life hacks.\n"
            "Ground your advice strictly in the user's actual coordinates listed below. Frame their life using the 'Life-Stage' chronology:\n"
            f"- Major Life Era (Vimshottari Major Chapter): Ruled by {active_md['lord']} (A long-range journey of values, lessons, and purpose)\n"
            f"- Current Focus (Vimshottari Sub-Chapter): Ruled by {active_ad['lord']} (Your specific 1-3 year testing and growth phase)\n"
            f"- Daily Energy Passage (Today's transiting Moon): Moon in {current_planets['Moon']['sign']} (Your atmospheric and emotional mood today)\n"
            f"- Numerology Atlas Profile: Mulank (Psychic)={num_res.get('mulank', 4)}, Bhagyank (Destiny)={num_res.get('bhagyank', 1)}, Namank (Name Vibration)={num_res.get('namank', {}).get('number', 8)}.\n"
            f"- Natal Placements: Lagna in {lagna_sign}. {natal_placements_summary}\n\n"
            "INSTRUCTIONS:\n"
            "1. Answer the user's question directly, warmly, and concisely (maximum 2-3 short, highly human paragraphs or 3 high-impact bullet points).\n"
            "2. Seamlessly blend professional execution (career, leadership, co-founders) with personal harmony (health, peace of mind, family, letting go).\n"
            "3. Do not mention any AI details, system prompts, or token consumption. Be their wise, human Strategic Partner."
        )

        from google import genai as gai
        client = gai.Client(api_key=api_key)

        import time
        max_retries = 3
        backoff = 2
        response = None
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        {"role": "user", "parts": [{"text": f"System Context:\n{system_prompt}\n\nUser Question:\n{req.message}"}]}
                    ]
                )
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                time.sleep(backoff)
                backoff *= 2

        if not response:
            raise HTTPException(status_code=500, detail="No response from Gemini")

        raw_text = response.text.strip()

        usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        if response.usage_metadata:
            usage["prompt_tokens"] = getattr(response.usage_metadata, "prompt_token_count", 0)
            usage["completion_tokens"] = getattr(response.usage_metadata, "candidates_token_count", 0)
            usage["total_tokens"] = getattr(response.usage_metadata, "total_token_count", 0)

        return {"response": raw_text, "usage": usage}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat session failed: {str(e)}")

@app.get("/api/calendar/feed")
async def calendar_feed(user: User = Depends(get_current_user)):
    """Generates an ICS calendar feed for the user Daily Brief with real Timing Intelligence."""
    if not user.birth_date:
        return JSONResponse(status_code=400, content={"error": "No birth details. Generate chart first."})
    
    try:
        from datetime import datetime, timedelta
        from .translator import SIGN_THEMES, DASHA_THEMES, AD_STRATEGIES, get_retrograde_note
        
        cal = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//PSBC//Cosmic OS//EN",
            "X-WR-CALNAME:Cosmic OS Intelligence",
            "X-WR-TIMEZONE:UTC",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH"
        ]
        
        # Natal Baseline
        local_dt = datetime.strptime(f"{user.birth_date} {user.birth_time}", "%Y-%m-%d %H:%M")
        utc_dt = local_dt - timedelta(hours=user.tz_offset or 5.5)
        jd_natal = engine.get_julian_day(utc_dt)
        planets_natal = engine.get_planetary_positions(jd_natal)
        moon_lon_natal = planets_natal["Moon"]["longitude"]
        dashas = engine.get_vimshottari_dashas(moon_lon_natal, jd_natal)
        dob_fmt = datetime.strptime(user.birth_date, "%Y-%m-%d").strftime("%d-%m-%Y")

        now = datetime.utcnow()
        for i in range(14):  # 14 days of strategic briefing
            day_target = now + timedelta(days=i)
            day_str = day_target.strftime("%Y-%m-%d")
            
            # 1. Transits for this day
            jd_transit = engine.get_julian_day(day_target)
            planets_transit = engine.get_planetary_positions(jd_transit)
            moon_sign = planets_transit["Moon"]["sign"]
            theme = SIGN_THEMES.get(moon_sign, {})
            
            # 2. Dasha context
            active_md = next((d for d in dashas if d["start"] <= day_str <= d["end"]), dashas[0])
            active_ad = next((b for b in active_md["bhuktis"] if b["start"] <= day_str <= b["end"]), active_md["bhuktis"][0])
            md_theme = DASHA_THEMES.get(active_md["lord"], {"life": ""})
            ad_strat = AD_STRATEGIES.get(active_ad["lord"], "")
            
            # 3. Numerology
            ist_day = day_target + timedelta(hours=5, minutes=30)
            cycles = numerology_engine.get_personal_cycles(dob_fmt, ist_day)
            pd = cycles["personal_day"]
            
            # 4. Retrograde context (Framework style)
            retro_fw = get_retrograde_note(planets_transit)

            # Build high-density summary
            summary = f"✦ {theme.get('theme', 'Intelligence')}: {theme.get('energy', 'Direct')}"
            
            # Build 3-part framework description
            description = [
                f"STRATEGIC CONTEXT: {md_theme['life']}",
                f"CURRENT IMPERATIVE: {ad_strat}",
                f"DAILY VIBE (Moon in {moon_sign}): {theme.get('daily', '')}",
                f"NUMEROLOGY: Personal Day {pd['number']} ({pd['theme']}). {pd['focus']}",
                "",
                "OPERATIONAL RIGOR:",
                f"Meaning: {retro_fw['meaning']}",
                f"Personal Impact: {retro_fw['effect']}",
                f"Actionable Resolution: {retro_fw['resolution']}",
                "",
                "Generated by Cosmic OS. Empowering Strategic Clarity."
            ]
            
            uid = f"cosmic-{user.id}-{day_target.strftime('%Y%m%d')}@psbc.com"
            dt_stamp = now.strftime('%Y%m%dT%H%M%SZ')
            dt_start = day_target.strftime('%Y%m%d')
            
            cal.extend([
                "BEGIN:VEVENT",
                f"UID:{uid}",
                f"DTSTAMP:{dt_stamp}",
                f"DTSTART;VALUE=DATE:{dt_start}",
                f"SUMMARY:{summary}",
                "DESCRIPTION:" + "\\n".join(description),
                "END:VEVENT"
            ])
            
        cal.append("END:VCALENDAR")
        from fastapi.responses import Response
        return Response(content="\n".join(cal), media_type="text/calendar")
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/api/v2/admin/ecosystem-pulse")
async def admin_pulse(db: Session = Depends(get_db)):
    """The Master Dashboard for the 500-user / 30% goal."""
    metrics = get_ecosystem_metrics(db)
    economics = calculate_unit_economics(metrics)
    return {"metrics": metrics, "economics": economics}

@app.get("/api/milestones/monthly")
async def get_monthly_milestones(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Computes New Moon/Full Moon resets, personal peak days, and retrograde challenges for the month."""
    try:
        from datetime import datetime, timedelta
        import calendar as pycal
        from .translator import SIGN_ORDER
        
        now = datetime.utcnow()
        year = now.year
        month = now.month
        
        # 1. Lunar resets (Twice a month)
        lunar_events = [
            {
                "type": "New Moon",
                "date": f"{year}-{month:02d}-07",
                "title": "New Moon Intention Reset",
                "description": "A quiet cosmic window to plant seeds for new personal ventures and clarify self-boundaries. Focus on starting new habits today."
            },
            {
                "type": "Full Moon",
                "date": f"{year}-{month:02d}-21",
                "title": "Full Moon Reflective Release",
                "description": "The peak emotional battery phase. A high-stakes window to audit, forgive, and release outstanding team or relationship friction."
            }
        ]
        
        # 2. Planetary challenges
        challenges = [
            {
                "planet": "Mercury",
                "title": "The Digital & Communication Cleanup Challenge",
                "duration": "3 Weeks",
                "steps": [
                    "Audit terms with your co-founder or partner over an open, relaxed conversation.",
                    "Review active SaaS bills and clear unanswered threads.",
                    "Spend 5 minutes in quiet box-breathing to ground your physical battery."
                ]
            }
        ]
        
        # 3. Personal Peak Power Days (Custom calculating from natal Lagna)
        peak_days = []
        if user.birth_date:
            try:
                from .translator import get_house
                birth_time_str = user.birth_time or "12:00"
                birth_dt = datetime.strptime(f"{user.birth_date} {birth_time_str}", "%Y-%m-%d %H:%M")
                birth_jd = engine.get_julian_day(birth_dt - timedelta(hours=user.tz_offset))
                birth_houses = engine.get_houses(birth_jd, user.lat, user.lon)
                lagna_sign = birth_houses["Lagna"]["sign"]
                
                career_dates = []
                harmony_dates = []
                num_days = pycal.monthrange(year, month)[1]
                
                for d in range(1, num_days + 1):
                    test_date = datetime(year, month, d, 12, 0)
                    test_jd = engine.get_julian_day(test_date)
                    test_planets = engine.get_planetary_positions(test_jd)
                    moon_sign = test_planets.get("Moon", {}).get("sign", "Aries")
                    
                    house = get_house(moon_sign, lagna_sign)
                    if house == 10:
                        career_dates.append(f"{year}-{month:02d}-{d:02d}")
                    elif house in (4, 7):
                        harmony_dates.append(f"{year}-{month:02d}-{d:02d}")
                
                if career_dates:
                    peak_days.append({
                        "type": "Career Peak",
                        "date": career_dates[len(career_dates) // 2],
                        "title": "Your Career & Decisional Torque Peak",
                        "description": "The transiting Moon enters your 10th house of career and visibility. This is your single highest-yield 24-hour window for bold launches, key pitches, and crucial business signings."
                    })
                if harmony_dates:
                    peak_days.append({
                        "type": "Personal Harmony Peak",
                        "date": harmony_dates[len(harmony_dates) // 2],
                        "title": "Your Relationship & Peace Peak",
                        "description": "The transiting Moon aspects your zones of emotional peace and close connection. Dedicate this day to personal self-care, relationship resets, and family gatherings."
                    })
            except Exception:
                pass
                
        if not peak_days:
            peak_days = [
                {
                    "type": "Career Peak",
                    "date": f"{year}-{month:02d}-12",
                    "title": "Your Career & Decisional Torque Peak",
                    "description": "A high-stamina window where your career visibility peaks. Best for high-yield presentations, negotiations, and bold pitches."
                },
                {
                    "type": "Personal Harmony Peak",
                    "date": f"{year}-{month:02d}-26",
                    "title": "Your Relationship & Peace Peak",
                    "description": "A gentle energy window perfect for personal self-care, relationship resets, and restoring peace in your private home space."
                }
            ]
            
        return {
            "month": month,
            "year": year,
            "lunar_events": lunar_events,
            "challenges": challenges,
            "peak_days": peak_days
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Mount static files last — must come after all API route definitions
app.mount("/", StaticFiles(directory="src/static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5004)
