# Jyotish Engine Core

A high-precision Vedic Astrology (Jyotish) engine built with FastAPI and PySwissEph.

## Features
- **Sidereal Calculations:** Uses Lahiri Ayanamsa by default.
- **Planetary Positions:** Computes Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu (Mean), and Ketu.
- **Lagna Calculation:** Accurate Ascendant based on birth time and location.
- **Minimalist UI:** Apple-inspired dashboard for easy data entry and visualization.

## Setup & Running

1. **Navigate to the directory:**
   ```bash
   cd jyotish-engine-core
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the server:**
   ```bash
   python -m src.main
   ```

5. **Access the UI:**
   Open `http://127.0.0.1:8000` in your browser.

## API Documentation
The API is available at `/api/chart`. It expects a POST request with the following JSON body:
```json
{
  "date": "YYYY-MM-DD",
  "time": "HH:MM",
  "lat": 28.6139,
  "lon": 77.2090,
  "timezone_offset": 5.5
}
```
