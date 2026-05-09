from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Query, Request, Depends, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from .engine import JyotishEngine
from .translator import generate_coach_insights, get_cosmic_schedule_advice, generate_business_pulse
from .auth.google_auth import GoogleAuthManager
from .auth.apple_auth import AppleAuthManager
from .integrations.gcal import GoogleCalendarManager
from .database.session import init_db, get_db
from .database.models import User, OAuthCredential, NumerologyProfile
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

@app.get("/auth/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("user_email")
    return response

# ── Google Auth ──

@app.get("/auth/google/login")
async def google_login(request: Request):
    """Initiates Google OAuth Flow."""
    redirect_uri = str(request.url_for("google_callback"))
    if not redirect_uri.startswith("https") and "localhost" not in redirect_uri and "127.0.0.1" not in redirect_uri:
        redirect_uri = redirect_uri.replace("http", "https")
        
    try:
        auth_url, state = google_auth.get_login_url(redirect_uri)
        return RedirectResponse(auth_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/auth/google/callback")
async def google_callback(request: Request, code: str = None, error: str = None, db: Session = Depends(get_db)):
    """Handles Google OAuth Callback and persists credentials."""
    if error:
        raise HTTPException(status_code=400, detail=f"Google Auth Error: {error}")
    if not code:
        raise HTTPException(status_code=400, detail="No code provided by Google.")
    
    redirect_uri = str(request.url_for("google_callback"))
    if not redirect_uri.startswith("https") and "localhost" not in redirect_uri and "127.0.0.1" not in redirect_uri:
        redirect_uri = redirect_uri.replace("http", "https")

    try:
        creds_dict = google_auth.exchange_code(code, redirect_uri)
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
    # This is a placeholder for the Apple JS-based flow initiation
    return JSONResponse({"info": "Use Sign in with Apple on the frontend"})

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
    has_creds = user.credentials is not None
    return {"authenticated": has_creds, "email": user.email}

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
        
        # 4. Standard Insights (natal chart + today's transit layer)
        insights = generate_coach_insights(planets, houses["Lagna"], current_planets)
        
        # 5. Nakshatra (birth Moon nakshatra)
        nakshatra = engine.get_nakshatra(planets["Moon"]["longitude"])

        # 6. Business ROI Pulse
        dashas = engine.get_vimshottari_dashas(planets["Moon"]["longitude"], jd)
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
                    
                    active_md_lord = dashas[0]["lord"] # Simplistic: first dasha in list is active
                    # Better: find the active one
                    date_now = now_utc.strftime("%Y-%m-%d")
                    active_md = next((d for d in dashas if d["start"] <= date_now <= d["end"]), dashas[0])
                    
                    cosmic_schedule = get_cosmic_schedule_advice(analyzed_events, current_planets, active_md["lord"])
                except Exception as e:
                    print(f"Calendar Integration Error: {e}")
        
        # 7. Advanced Astrology Calculation Layer
        yogas             = detect_yogas(planets, houses["Lagna"])
        sade_sati         = check_sade_sati(planets["Moon"]["sign"], current_planets["Saturn"]["sign"])
        mangal_dosha      = check_mangal_dosha(planets, houses["Lagna"])
        ashtakavarga      = calculate_ashtakavarga(planets, houses["Lagna"])
        divisional_charts = calculate_divisional_charts(planets, houses["Lagna"])
        varshaphal        = calculate_varshaphal(planets["Sun"]["longitude"], details.lat, details.lon)

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

        from .translator import generate_business_pulse
        pulse = generate_business_pulse(dashas, datetime.utcnow())
        active_dasha = pulse.get("active_dasha", "Sun-Sun")

        advice = get_timing_advice(active_dasha, current_planets, nakshatra.get("nakshatra", ""))
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

        from .translator import generate_business_pulse
        pulse = generate_business_pulse(dashas, datetime.utcnow())
        active_dasha = pulse.get("active_dasha", "Sun-Sun")

        dob_formatted = datetime.strptime(user.birth_date, "%Y-%m-%d").strftime("%d-%m-%Y")
        today_ist = datetime.utcnow() + timedelta(hours=5, minutes=30)
        cycles = numerology_engine.get_personal_cycles(dob_formatted, today_ist)

        timing = get_timing_advice(active_dasha, current_planets, nakshatra.get("nakshatra", ""))
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


@app.get("/api/chart/muhurta")
async def get_muhurta(days: int = Query(7, ge=1, le=30)):
    """Return auspicious windows for the next N days (IST)."""
    try:
        windows = calculate_muhurta(days)
        return {"muhurta_windows": windows, "days_ahead": days}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files last — must come after all API route definitions
# because app.mount("/") is a catch-all that intercepts anything not yet matched.
app.mount("/", StaticFiles(directory="src/static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5004)

@app.get("/api/calendar/feed")
async def calendar_feed(user: User = Depends(get_current_user)):
    """Generates an ICS calendar feed for the user Daily Brief."""
    if not user.birth_date:
        return {"error": "No birth details. Generate chart first."}
    
    try:
        from datetime import datetime, timedelta
        cal = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//PSBC//Cosmic OS//EN",
            "X-WR-CALNAME:Cosmic OS Intelligence",
            "X-WR-TIMEZONE:UTC",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH"
        ]
        
        now = datetime.utcnow()
        for i in range(14):  # 14 days of feed
            day = now + timedelta(days=i)
            # Basic event for morning brief
            uid = f"brief-{user.id}-{day.strftime('%Y%m%d')}@psbc.com"
            dt_str = day.strftime('%Y%m%d')
            
            # Simple placeholder text - in reality we would call the engines here
            summary = f"✨ Cosmic Brief - Day {i}"
            desc = "Open Cosmic OS to see your full strategic intelligence for today."
            
            cal.extend([
                "BEGIN:VEVENT",
                f"UID:{uid}",
                f"DTSTAMP:{now.strftime('%Y%m%dT%H%M%SZ')}",
                f"DTSTART;VALUE=DATE:{dt_str}",
                f"SUMMARY:{summary}",
                f"DESCRIPTION:{desc}",
                "END:VEVENT"
            ])
            
        cal.append("END:VCALENDAR")
        from fastapi.responses import Response
        return Response(content="\n".join(cal), media_type="text/calendar")
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/v2/admin/ecosystem-pulse")
async def admin_pulse(db: Session = Depends(get_db)):
    """The Master Dashboard for the 500-user / 30% goal."""
    metrics = get_ecosystem_metrics(db)
    economics = calculate_unit_economics(metrics)
    return {"metrics": metrics, "economics": economics}
