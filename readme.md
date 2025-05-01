# 🔮 Astrological Toolbox

Astrological Toolbox is a suite of interactive astrology tools built with Python and Streamlit, using precise calculations based on the Swiss Ephemeris (SWE).

---

## 📁 Project Structure

```
📁 root/
├️️ app.py                   # Main entry point for the Streamlit app
├️️ README.md                # This file
├️️ requirements.txt         # List of dependencies
├️️ .gitignore               # Files to exclude from Git
├️️ .env                     # Environment variables (excluded from Git)
│
📁 ui/                     # Visual components and helper functions
│   └️️ display.py
│
📁 pages/                  # Streamlit multipage layout
│   ├️️ 1_Data_Input.py     # User input for birth data
│   ├️️ 2_Natal_Chart.py    # Natal chart visualization
│   ├️️ 3_Progressed_Chart.py # Secondary progressions
│   └️️ 9_Settings.py       # App settings
│
📁 backend/                # Low-level astrological logic
│   └️️ ephemeris.py        # Swiss Ephemeris integration
│
📁 controller/             # Business logic and data coordination
│   ├️️ astro.py
│   ├️️ progressions.py
│   └️️ time_utils.py
│
📁 services/               # External integrations
│   └️️ geolocation.py      # Location & timezone lookup via API
│
📁 config/                 # Static data loading and session setup
│   ├️️ loaders.py
│   └️️ init_session.py
│
📁 data/                   # Static JSON data
    ├️️ aspects.json
    ├️️ houses.json
    ├️️ planets.json
    └️️ signs.json
```

---

## 🚀 Technologies Used

- [Streamlit](https://streamlit.io/) – Web framework for interactive apps
- [Swiss Ephemeris (swisseph)](https://www.astro.com/swisseph/) – High-precision ephemeris
- [OpenCage Geocoder](https://opencagedata.com/) – Geolocation and timezone lookup
- [Pandas](https://pandas.pydata.org/) – Data manipulation

---

## 🎯 Purpose

This project aims to support astrologers with digital tools for natal chart analysis and astrological calculations. Current and future features include:

- Natal chart generation
- Aspect calculations
- Upcoming features: current transits, time-range transits, synastry, secondary progressions, fixed stars, lots, dissociative aspect filtering, solar return analysis, composite charts, planetary dignities

---

## ▶️ How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/astro-toolbox.git
   cd astro-toolbox
   ```

2. **Set up your environment variables:**
   Create a `.env` file with your OpenCage API key:
   ```env
   GEO_API_KEY='your_opencage_api_key_here'
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the application:**
   ```bash
   streamlit run app.py
   ```

---

## 🔐 Environment Variables

If you’re deploying on [Streamlit Cloud](https://streamlit.io/cloud), add the following **as a secret**:

- `GEO_API_KEY` – Your OpenCage API Key

---

## 📄 License

*Add your preferred license here (MIT, GPL, etc).*

---

📬 *For questions, suggestions, or contributions, feel free to reach out to the project author.*

