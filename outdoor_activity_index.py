# outdoor_activity_index.py
# Calculates the outdoor activity index based on weather data.

# =======================================
# 1. 감점 요인 정의 (영문/한글)
# =======================================
REASON_MAPPING_EN = {
    "temperature": "High Temp",
    "humidity": "Humid",
    "wind": "Strong Wind",
    "precipitation": "Rain Likely",
    "air_quality": "Bad Air",
    "uv_index": "Strong UV",
    "sky": "Too Sunny"
}

REASON_MAPPING_KO = {
    "temperature": "높은 기온",
    "humidity": "높은 습도",
    "wind": "강한 바람",
    "precipitation": "강수 확률",
    "air_quality": "나쁜 대기질",
    "uv_index": "높은 UV 지수",
    "sky": "강한 햇빛"
}

# =======================================
# 2. 개별 점수 계산 함수 (기존과 동일)
# =======================================

def _score_temperature(temp, mode):
    """온도 점수 계산 (30점 만점)"""
    score = 0
    if mode == "summer": # 덥거나 따뜻한 날
        if 18 <= temp <= 24: score = 30
        elif 15 <= temp < 18 or 24 < temp <= 26: score = 25
        elif 12 <= temp < 15 or 26 < temp <= 28: score = 20
        elif 28 < temp <= 30: score = 10
        else: score = 5
    elif mode == "winter": # 추운 날
        if 5 <= temp <= 10: score = 30
        elif 2 <= temp < 5 or 10 < temp <= 12: score = 25
        elif -1 <= temp < 2 or 12 < temp <= 14: score = 20
        elif -5 <= temp < -1: score = 10
        else: score = 5
    else: # 온화한 날 (봄/가을)
        if 14 <= temp <= 20: score = 30
        elif 11 <= temp < 14 or 20 < temp <= 22: score = 25
        elif 8 <= temp < 11 or 22 < temp <= 24: score = 20
        else: score = 10
    return score

def _score_humidity(humidity):
    """습도 점수 계산 (20점 만점)"""
    if 40 <= humidity <= 60: return 20
    elif 30 <= humidity < 40 or 60 < humidity <= 70: return 15
    elif 70 < humidity <= 80: return 10
    else: return 5

def _score_wind(wind, mode):
    """바람 점수 계산 (10점 만점, 계절별 로직)"""
    if mode == "summer": # 더울 땐 바람이 긍정적
        if 2 <= wind <= 4: return 10
        elif wind < 2: return 8
        elif 4 < wind <= 6: return 6
        else: return 2
    elif mode == "winter": # 추울 땐 바람이 부정적
        if wind < 1: return 10
        elif 1 <= wind < 3: return 5
        else: return 0
    else: # 온화한 날
        if wind < 3: return 10
        elif 3 <= wind < 6: return 7
        elif 6 <= wind < 9: return 4
        else: return 2

def _score_precipitation(prob, amount):
    """강수 점수 계산 (25점 만점)"""
    prob_score = 0
    if prob <= 10: prob_score = 15
    elif prob <= 30: prob_score = 10
    elif prob <= 50: prob_score = 5
    else: prob_score = 0

    amount_score = 0
    if amount < 0.5: amount_score = 10
    elif amount < 1: amount_score = 7
    elif amount < 3: amount_score = 4
    else: amount_score = 0
    
    return prob_score + amount_score

def _score_air_quality(air_quality_status):
    """공기질 점수 계산 (15점 만점)"""
    # 한국어/영어 상태 모두 처리
    status_lower = str(air_quality_status).lower()
    if "good" in status_lower or "좋음" in status_lower: return 15
    elif "moderate" in status_lower or "보통" in status_lower: return 10
    elif "bad" in status_lower or "나쁨" in status_lower: return 5
    else: return 0

def _get_bonus_penalty(uvi, sky_status):
    """오전 시간대 보너스/패널티 점수 계산"""
    score = 0
    if uvi is None: uvi = 0
        
    if uvi <= 2: score += 5
    elif 6 <= uvi <= 7: score -= 2
    elif uvi >= 8: score -= 5
    
    if sky_status in ["Cloudy", "Overcast", "흐림"]:
        score += 5
    return score

# =======================================
# 3. 메인 계산 함수 (다국어 지원 추가)
# =======================================

def calculate_activity_index(weather_data, time_slot, daily_max_temp, daily_uv_max, daily_air_quality, language='en'):
    """
    야외활동 지수를 계산하고 지정된 언어로 결과를 반환합니다.
    """
    
    # 1. 계절 모드 결정
    if daily_max_temp >= 23: mode = "summer"
    elif daily_max_temp <= 10: mode = "winter"
    else: mode = "mild"

    # 2. 시간대별 데이터 추출
    if time_slot == 'am': start, end = 600, 900
    else: start, end = 1800, 2100

    temps = [t['value'] for t in weather_data.get('temperatures', []) if start <= t['time'] <= end]
    humi = [h['value'] for h in weather_data.get('humidity', []) if start <= h['time'] <= end]
    wind = [w['value'] for w in weather_data.get('wind_speeds', []) if start <= w['time'] <= end]
    rain_prob = {t: p for t, p in weather_data.get('rain_prob', {}).items() if start <= t <= end}
    rain_amounts = [a for t, a in weather_data.get('rain_amount', {}).items() if start <= t <= end]
    sky = {t: s for t, s in weather_data.get('sky_status', {}).items() if start <= t <= end}

    avg_temp = sum(temps) / len(temps) if temps else 0
    avg_humi = sum(humi) / len(humi) if humi else 50
    avg_wind = sum(wind) / len(wind) if wind else 0
    max_rain_prob = max(rain_prob.values()) if rain_prob else 0
    total_rain_amount = sum(rain_amounts) if rain_amounts else 0
    avg_sky_val = sum(sky.values()) / len(sky) if sky else 1
    
    sky_status = "Sunny"
    if avg_sky_val >= 4: sky_status = "Overcast"
    elif avg_sky_val >= 3: sky_status = "Cloudy"

    # 3. 점수 및 감점 계산
    scores = {}
    penalties = {}

    scores['temperature'] = _score_temperature(avg_temp, mode)
    penalties['temperature'] = 30 - scores['temperature']
    scores['humidity'] = _score_humidity(avg_humi)
    penalties['humidity'] = 20 - scores['humidity']
    scores['wind'] = _score_wind(avg_wind, mode)
    penalties['wind'] = 10 - scores['wind']
    scores['precipitation'] = _score_precipitation(max_rain_prob, total_rain_amount)
    penalties['precipitation'] = 25 - scores['precipitation']
    scores['air_quality'] = _score_air_quality(daily_air_quality)
    penalties['air_quality'] = 15 - scores['air_quality']

    total_score = sum(scores.values())

    if time_slot == 'am':
        bonus = _get_bonus_penalty(daily_uv_max, sky_status)
        total_score += bonus
        if bonus < 0: penalties['uv_index'] = abs(bonus)

    # 4. 최종 등급 및 감점 요인 결정 (언어별)
    grades_en = {90: "Excellent", 75: "Good", 60: "Moderate", 45: "Bad", 0: "Very Bad"}
    grades_ko = {90: "최상", 75: "좋음", 60: "보통", 45: "나쁨", 0: "매우 나쁨"}
    grades = grades_ko if language == 'ko' else grades_en
    
    final_grade = grades[0] # 기본값
    for score_threshold, grade_text in sorted(grades.items(), reverse=True):
        if total_score >= score_threshold:
            final_grade = grade_text
            break

    reason = None
    if final_grade in ["Moderate", "Bad", "Very Bad", "보통", "나쁨", "매우 나쁨"]:
        if penalties:
            worst_factor = max(penalties, key=penalties.get)
            if penalties[worst_factor] > 5:
                reason_map = REASON_MAPPING_KO if language == 'ko' else REASON_MAPPING_EN
                reason = reason_map.get(worst_factor)

    return {"grade": final_grade, "reason": reason}

# 테스트 함수는 변경 없음
def get_mock_data(scenario="good_day"):
    # ... (기존 코드와 동일)
    pass

def test_activity_index():
    # ... (기존 코드와 동일)
    pass

if __name__ == "__main__":
    test_activity_index()
