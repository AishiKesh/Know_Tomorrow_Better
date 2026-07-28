import math
import datetime

ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

def calculate_astronomy_engine(birth_date: datetime.date, birth_time: datetime.time) -> dict:
    """
    Computes approximate geocentric ecliptic longitudes for the Sun and Moon
    based on standard low-precision tracking formulas (J2000 Epoch).
    """
    # Combine date and time into a single datetime object
    dt = datetime.datetime.combine(birth_date, birth_time)
    
    # Calculate Julian Date (approximate fraction days since Jan 1, 2000, 12:00 UT)
    time_tuple = dt.utctimetuple()
    year, month, day = time_tuple.tm_year, time_tuple.tm_mon, time_tuple.tm_mday
    hour = time_tuple.tm_hour + time_tuple.tm_min / 60.0 + time_tuple.tm_sec / 3600.0
    
    if month <= 2:
        year -= 1
        month += 12
    A = int(year / 100)
    B = 2 - A + int(A / 4)
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + (hour / 24.0) + B - 1524.5
    d = jd - 2451545.0  # Days past J2000.0

    # --- SUN CALCULATIONS ---
    g = math.radians((357.529 + 0.98560028 * d) % 360)
    q = 280.459 + 0.98564736 * d
    sun_long = (q + 1.915 * math.sin(g) + 0.020 * math.sin(2 * g)) % 360
    sun_idx = int(sun_long // 30)

    # --- MOON CALCULATIONS ---
    moon_mean_long = 218.316 + 13.176396 * d
    moon_mean_anom = math.radians((134.963 + 13.064993 * d) % 360)
    moon_elongation = math.radians((297.850 + 12.190749 * d) % 360)
    
    moon_long = (moon_mean_long + 6.289 * math.sin(moon_mean_anom) + 1.274 * math.sin(2 * moon_elongation - moon_mean_anom)) % 360
    moon_idx = int(moon_long // 30)

    # --- REAL-TIME TEMPORAL TRANSIT MATRIX GENERATOR ---
    current_days_past = (datetime.datetime.utcnow() - datetime.datetime(2000, 1, 1, 12, 0)).days
    jupiter_approx_long = (22.22 + 0.083 * current_days_past) % 360
    saturn_approx_long = (274.12 + 0.033 * current_days_past) % 360
    
    jupiter_house = int((jupiter_approx_long // 30) % 12) + 1
    
    transits = []
    if abs((saturn_approx_long % 90) - (moon_long % 90)) < 8:
        transits.append(f"Saturn Square Natal Moon (Active Resistance at {int(saturn_approx_long)}°)")
    else:
        transits.append(f"Saturn Transiting the {ZODIAC_SIGNS[int(saturn_approx_long//30)]} quadrant")
        
    transits.append(f"Jupiter Transiting your {jupiter_house} House of financial expansion")

    return {
        "sun_sign": ZODIAC_SIGNS[sun_idx],
        "moon_sign": ZODIAC_SIGNS[moon_idx],
        "transits": transits
    }