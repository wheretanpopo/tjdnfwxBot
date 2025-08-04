# forecast_generator.py
# Generates final forecast results (dictionaries, text) from processed data.
# 처리된 데이터를 분석하여 최종 날씨 요약 정보를 생성합니다.

import datetime

def get_base_datetime():
    """API 호출을 위한 기준 날짜와 시간을 결정합니다."""
    now = datetime.datetime.now()
    base_dt = now - datetime.timedelta(hours=3)
    available_times = [2, 5, 8, 11, 14, 17, 20, 23]
    
    # base_dt의 시간(hour)을 기준으로 가장 가까운 과거의 available_time을 찾음
    target_hour = None
    for t in sorted(available_times, reverse=True):
        if base_dt.hour >= t:
            target_hour = t
            break
            
    # 만약 base_dt.hour가 모든 available_times보다 작으면 (예: base_dt.hour가 0 또는 1일 때)
    # 이는 전날의 마지막 available_time (23시)을 사용해야 함을 의미
    if target_hour is None:
        target_hour = 23 # 전날 23시
        base_dt = base_dt - datetime.timedelta(days=1) # 날짜를 전날로 변경

    base_date_str = base_dt.strftime("%Y%m%d")
    base_time_str = f"{target_hour:02d}00"
    
    return base_date_str, base_time_str

def classify_wind_strength(wind_speed):
    """
    바람 강도를 분류합니다.
    
    Args:
        wind_speed: 풍속 (m/s)
    
    Returns:
        dict: {"strength": "강도", "description": "설명"}
    """
    if wind_speed <= 1:
        return {"strength": "고요", "description": "바람이 거의 없어요"}
    elif wind_speed <= 3:
        return {"strength": "미풍", "description": "가벼운 바람이 불어요"} 
    elif wind_speed <= 6:
        return {"strength": "바람", "description": "바람이 조금 불어요"}
    elif wind_speed <= 10:
        return {"strength": "강한바람", "description": "바람이 강하게 불어요"}
    else:
        return {"strength": "강풍", "description": "매우 강한 바람이 불어요"}

def classify_main_weather(sky_status, rain_type, rain_prob_max, temp_max, rainfall_max=0, warnings=None):
    """
    전체적인 날씨 상태를 분류합니다. 특보를 최우선으로 고려하되, 다른 날씨 정보도 함께 반환합니다.
    """
    print(f"[DEBUG] classify_main_weather received warnings: {warnings}")
    
    special_weather = None
    special_description = None

    # 1. 기상청 공식 특보 우선 판단
    if warnings and isinstance(warnings, dict):
        warn_type = str(warnings.get('type', '')).strip().replace('\r', '').replace('\n', '')
        print(f"[DEBUG] Processed warn_type: '{warn_type}'")

        if warn_type == '폭염':
            print("[DEBUG] '폭염' 특보 조건 일치! HEATWAVE 설정.")
            special_weather = "HEATWAVE"
            special_description = f"폭염 {warnings.get('level', '')} 발효 중"
        elif warn_type == '호우':
            print("[DEBUG] '호우' 특보 조건 일치! HEAVY_RAIN 설정.")
            special_weather = "HEAVY_RAIN"
            special_description = f"호우 {warnings.get('level', '')} 발효 중"
        elif warn_type == '태풍':
            print("[DEBUG] '태풍' 특보 조건 일치! TYPHOON 설정.")
            special_weather = "TYPHOON"
            special_description = f"태풍 {warnings.get('level', '')} 발효 중"

    # --- 항상 일반 날씨 판단 로직을 수행 ---
    base_weather = None
    temp_state = "NORMAL"
    
    # 2. 강수 상태 판단
    if any(t == 4 for t in rain_type.values()):
        base_weather = "SHOWER"
    elif any(t == 3 for t in rain_type.values()):
        base_weather = "SNOW"
    elif any(t > 0 for t in rain_type.values()) or rain_prob_max >= 50:
        base_weather = "RAINY"
    
    # 3. 하늘 상태 판단 (강수 없을 때)
    if base_weather is None:
        avg_sky = sum(sky_status.values()) / len(sky_status) if sky_status else 1
        if avg_sky <= 2:
            base_weather = "SUNNY"
        elif avg_sky <= 3:
            base_weather = "PARTLY_CLOUDY"
        else:
            base_weather = "CLOUDY"
    
    # 4. 온도 상태 판단
    if temp_max is not None:
        if temp_max >= 32:
            temp_state = "VERY_HOT"
        elif temp_max >= 28:
            temp_state = "HOT"
        elif temp_max <= 5:
            temp_state = "VERY_COLD"
        elif temp_max <= 10:
            temp_state = "COLD"
    
    # 5. 최종 결과 조합
    # 기본 날씨 설명 생성
    base_desc_map = {
        "SUNNY": "맑음", "PARTLY_CLOUDY": "구름 조금", "CLOUDY": "흐림",
        "RAINY": "비", "SNOW": "눈", "SHOWER": "소나기"
    }
    temp_desc_map = {
        "VERY_HOT": "매우 더움", "HOT": "더움", "COLD": "쌀쌀함", "VERY_COLD": "매우 추움"
    }
    
    base_description = base_desc_map.get(base_weather, "")
    if temp_state != "NORMAL":
        temp_description = temp_desc_map.get(temp_state, "")
        base_description = f"{base_description}, {temp_description}" if base_description else temp_description

    # 특보가 있으면 특보를 최종 날씨 상태로 사용
    if special_weather:
        final_weather = special_weather
        final_description = special_description
        if final_weather in ["HEATWAVE", "TYPHOON"]:
            temp_state = "EXTREME"
        else:
            temp_state = "NORMAL"
        combined = final_weather
    else:
        final_weather = base_weather
        final_description = base_description
        if temp_state != "NORMAL":
            combined = f"{base_weather}_{temp_state}"
        else:
            combined = base_weather

    return {
        "weather": final_weather,
        "temperature": temp_state,
        "combined": combined,
        "description": final_description,
        "base_description": base_description # 기본 날씨 설명 추가
    }

def analyze_processed_data(processed_data, target_date, yesterday_temps=None, warnings=None, language='en'):
    """
    처리된 날씨 데이터를 종합 분석하여 최종 요약을 생성합니다.
    계절에 따라 온도 비교 기준을 변경하고, 새로운 정보들을 추가합니다.
    
    Args:
        language (str): 'en' 또는 'ko' - 강수 정보 등의 언어를 결정
    """
    
    print(f" -> 날씨 데이터 종합 분석 시작 ({language.upper()})...")
    
    summary = {}
    date_obj = datetime.datetime.strptime(target_date, "%Y%m%d")
    month = date_obj.month

    # ============================================
    # 1. 기본 데이터 추출
    # ============================================
    all_temps_data = processed_data.get('temperatures', [])
    temps = [t['value'] for t in all_temps_data]
    summary['temp_max'] = processed_data.get('temp_max') or (max(temps) if temps else None)
    summary['temp_min'] = processed_data.get('temp_min') or (min(temps) if temps else None)

    humidity_data = processed_data.get('humidity', [])
    humidity_values = [h['value'] for h in humidity_data]
    summary['avg_humidity'] = round(sum(humidity_values) / len(humidity_values), 1) if humidity_values else 0

    wind_data = processed_data.get('wind_speeds', [])
    wind_values = [w['value'] for w in wind_data]
    summary['max_wind_speed'] = round(max(wind_values), 1) if wind_values else 0

    # ============================================
    # 2. 계절별 온도차 및 신규 정보 계산 (언어별)
    # ============================================
    summary['temp_diff'] = None
    summary['temp_diff_description'] = ""

    if yesterday_temps:
        # 겨울 (12, 1, 2월)에는 최저기온 비교
        if month in [12, 1, 2]:
            yesterday_min = yesterday_temps.get('yesterday_min_temp')
            if yesterday_min is not None and summary['temp_min'] is not None:
                temp_diff = round(summary['temp_min'] - yesterday_min, 1)
                summary['temp_diff'] = temp_diff
                if language == 'ko':
                    if temp_diff > 0:
                        summary['temp_diff_description'] = f"어제 아침보다 {temp_diff}°C 포근해요"
                    elif temp_diff < 0:
                        summary['temp_diff_description'] = f"어제 아침보다 {abs(temp_diff)}°C 더 추워요"
                    else:
                        summary['temp_diff_description'] = "어제 아침과 비슷해요"
                else:
                    if temp_diff > 0:
                        summary['temp_diff_description'] = f"{temp_diff}°C warmer than yesterday morning"
                    elif temp_diff < 0:
                        summary['temp_diff_description'] = f"{abs(temp_diff)}°C colder than yesterday morning"
                    else:
                        summary['temp_diff_description'] = "Similar to yesterday morning"
        # 그 외 계절에는 최고기온 비교
        else:
            yesterday_max = yesterday_temps.get('yesterday_max_temp')
            if yesterday_max is not None and summary['temp_max'] is not None:
                temp_diff = round(summary['temp_max'] - yesterday_max, 1)
                summary['temp_diff'] = temp_diff
                if language == 'ko':
                    if temp_diff > 0:
                        summary['temp_diff_description'] = f"어제 낮보다 {temp_diff}°C 더 더워요"
                    elif temp_diff < 0:
                        summary['temp_diff_description'] = f"어제 낮보다 {abs(temp_diff)}°C 더 시원해요"
                    else:
                        summary['temp_diff_description'] = "어제 낮과 비슷해요"
                else:
                    if temp_diff > 0:
                        summary['temp_diff_description'] = f"{temp_diff}°C hotter than yesterday"
                    elif temp_diff < 0:
                        summary['temp_diff_description'] = f"{abs(temp_diff)}°C cooler than yesterday"
                    else:
                        summary['temp_diff_description'] = "Similar to yesterday"

    # 일교차 계산
    if summary['temp_max'] is not None and summary['temp_min'] is not None:
        summary['diurnal_range'] = round(summary['temp_max'] - summary['temp_min'], 1)
    else:
        summary['diurnal_range'] = None

    # 불쾌지수 계산
    if summary['temp_max'] is not None and summary['avg_humidity'] > 0:
        t = summary['temp_max']
        h = summary['avg_humidity']
        discomfort_index = (9/5 * t) - 0.55 * (1 - h/100) * ((9/5 * t) - 26) + 32
        summary['discomfort_index'] = round(discomfort_index, 1)
        if language == 'ko':
            if discomfort_index >= 80:
                summary['discomfort_level'] = "매우 높음"
            elif discomfort_index >= 75:
                summary['discomfort_level'] = "높음"
            elif discomfort_index >= 68:
                summary['discomfort_level'] = "보통"
            else:
                summary['discomfort_level'] = "낮음"
        else:
            if discomfort_index >= 89:
                summary['discomfort_level'] = "Very High"
            elif discomfort_index >= 80:
                summary['discomfort_level'] = "High"
            elif discomfort_index >= 70:
                summary['discomfort_level'] = "Moderate"
            else:
                summary['discomfort_level'] = "Low"
    else:
        summary['discomfort_index'] = None
        summary['discomfort_level'] = "N/A"

    # 밤 9시~12시 하늘 상태 조회 (언어별)
    sky_status_data = processed_data.get('sky_status', {})
    night_sky_codes = [v for k, v in sky_status_data.items() if 2100 <= k <= 2359]
    if night_sky_codes:
        avg_night_sky = sum(night_sky_codes) / len(night_sky_codes)
        if language == 'ko':
            if avg_night_sky <= 1.5:
                summary['night_sky_clarity'] = "매우 맑음"
            elif avg_night_sky <= 2.5:
                summary['night_sky_clarity'] = "구름 조금"
            else:
                summary['night_sky_clarity'] = "흐림"
        else:
            if avg_night_sky <= 1.5:
                summary['night_sky_clarity'] = "Very Clear"
            elif avg_night_sky <= 2.5:
                summary['night_sky_clarity'] = "Partly Cloudy"
            else:
                summary['night_sky_clarity'] = "Cloudy"
    else:
        summary['night_sky_clarity'] = "정보 없음" if language == 'ko' else "No Data"

    # ============================================
    # 3. 나머지 정보 분석 (바람, 강수 등)
    # ============================================
    wind_info = classify_wind_strength(summary['max_wind_speed'])
    summary['wind_strength'] = wind_info['strength']
    summary['wind_description'] = wind_info['description']

    rain_prob = processed_data.get('rain_prob', {})
    rain_amounts = processed_data.get('rain_amounts_list', [])
    rain_type = processed_data.get('rain_type', {})
    summary['rain_prob_max'] = max(rain_prob.values()) if rain_prob else 0
    summary['rainfall_max'] = max(rain_amounts) if rain_amounts else 0
    summary['total_rain_amount'] = round(sum(rain_amounts), 1) if summary['rain_prob_max'] >= 30 and rain_amounts else 0
    
    rain_times = sorted([t for t, p in rain_prob.items() if p >= 30])
    if rain_times:
        start_time = f"{rain_times[0]:04d}"[:2] + ("시" if language == 'ko' else ":00")
        end_time = f"{rain_times[-1]+100:04d}"[:2] + ("시" if language == 'ko' else ":00")
        rain_amount_data = {t:a for t, a in processed_data.get('rain_amount', {}).items() if t in rain_times}
        peak_time = max(rain_amount_data, key=rain_amount_data.get) if rain_amount_data else None
        peak_time_str = f"{peak_time:04d}"[:2] + ("시경" if language == 'ko' else ":00") if peak_time else ""
        
        if language == 'ko':
            summary['rainfall_summary'] = f"{start_time}~{end_time} (피크: {peak_time_str})"
        else:
            summary['rainfall_summary'] = f"{start_time}~{end_time} (Peak: {peak_time_str})"
    else:
        summary['rainfall_summary'] = "비 소식 없음" if language == 'ko' else "No rain expected"

    # 강수 시간대 상세 분석 (언어별로 처리)
    summary['detailed_rain_times'] = analyze_rain_times_detailed(
        rain_prob, {}, rain_type, 
        {0:"No rain", 1:"Rain", 2:"Rain/Snow", 3:"Snow", 4:"Showers"},
        language=language
    )

    # ============================================
    # 4. 전체 날씨 상태 분류 (기존 로직 유지)
    # ============================================
    main_weather_info = classify_main_weather(
        sky_status_data, rain_type, summary['rain_prob_max'], 
        summary['temp_max'], summary['rainfall_max'], warnings=warnings
    )
    summary.update(main_weather_info)
    
    print(f" -> 날씨 데이터 종합 분석 완료 ({language.upper()})!")
    print(f"    - 온도차: {summary.get('temp_diff_description')}")
    print(f"    - 일교차: {summary.get('diurnal_range')}°C")
    print(f"    - 불쾌지수: {summary.get('discomfort_index')} ({summary.get('discomfort_level')})")
    print(f"    - 밤 9-12시 하늘: {summary.get('night_sky_clarity')}")
    print(f"    - 강수 요약: {summary.get('rainfall_summary')}")

    return summary

# 기존 함수들 (analyze_rain_times_detailed, create_instagram_summary) 유지
def analyze_rain_times_detailed(prob, amount, p_type, pty_map, language='en'):
    """
    강수 시간, 확률, 형태를 분석하여 상세 텍스트 리스트를 반환합니다.
    """
    
    def group_times(times):
        if not times:
            return []
        groups = []
        current_group = [times[0]]
        for i in range(1, len(times)):
            if (times[i] - current_group[-1]) <= 100:
                current_group.append(times[i])
            else:
                groups.append(current_group)
                current_group = [times[i]]
        groups.append(current_group)
        return groups

    def format_group_string(g, include_type=True):
        start_hour = f"{g[0]:04d}"[:2]
        end_hour = f"{g[-1]:04d}"[:2]
        time_str = f"{start_hour}:00" if start_hour == end_hour else f"{start_hour}:00-{int(end_hour)+1:02d}:00"
        
        type_str = ""
        if include_type:
            types_in_group = [p_type.get(t, 0) for t in g if p_type.get(t, 0) > 0]
            main_type_code = max(set(types_in_group), key=types_in_group.count) if types_in_group else 0
            type_str = pty_map.get(main_type_code, "")
        
        return f"{time_str} ({type_str})" if type_str and type_str != "No rain" and type_str != "강수 없음" else time_str

    details = []
    
    if language == 'ko':
        pty_map = {0: "강수 없음", 1: "비", 2: "비/눈", 3: "눈", 4: "소나기"}
        high_chance_label = "강수 예상(50%↑):"
        possible_label = "강수 가능(30%↑):"
    else:
        high_chance_label = "HIGH CHANCE OF RAIN:"
        possible_label = "POSSIBLE RAIN:"

    # 50% 이상 (높은 확률)
    high_prob_times = sorted([t for t, p in prob.items() if p >= 50])
    if high_prob_times:
        high_prob_groups = group_times(high_prob_times)
        formatted_groups = [format_group_string(g, include_type=True) for g in high_prob_groups]
        details.append(f"{high_chance_label} {', '.join(formatted_groups)}".upper())

    # 30% 이상 50% 미만 (가능성 있음)
    possible_rain_times = sorted([t for t, p in prob.items() if 30 <= p < 50])
    if possible_rain_times:
        possible_rain_groups = group_times(possible_rain_times)
        formatted_groups = [format_group_string(g, include_type=False) for g in possible_rain_groups]
        details.append(f"{possible_label} {', '.join(formatted_groups)}".upper())

    return details

def create_instagram_summary(data, catch_phrase):
    """기존 인스타그램 요약 함수 (일부 수정)"""
    target_dt = datetime.datetime.strptime(data['info']['target_date'], "%Y%m%d")
    
    parts = [f"✨ Today's Weather ({target_dt.strftime('%b %d')})"]
    parts.append(f"> {catch_phrase}")

    min_t = int(data['weather_summary'].get('temp_min', 0))
    max_t = int(data['weather_summary'].get('temp_max', 0))
    parts.append(f"🌡️ Temp: {min_t}°C ~ {max_t}°C")
    
    rain_info = data['weather_summary']['detailed_rain_times']
    parts.append(f"💧 Precip: {', '.join(rain_info)}")

    parts.append(f"💨 Wind: {data['weather_summary']['max_wind_speed']} m/s | Humidity: {data['weather_summary']['avg_humidity']}% ")
    air_quality_info = data['indices'].get('air_quality', {'status': 'N/A'})
    air_quality_status = air_quality_info.get('status', 'N/A')
    parts.append(f"🍃 Air Quality: {air_quality_status} | UV Index: {data['indices'].get('uv_index', 'N/A')}")
    
    astro = data['astro_info']
    parts.append(f"🌅 Sunrise {astro.get('sunrise', 'N/A')} | 🌇 Sunset {astro.get('sunset', 'N/A')}")
    parts.append(f"🌕 Moon: {astro.get('moon_phase_simple', 'N/A')}")

    hashtags = "#weatherforecast #dailyweather #seoulweather #weathergram"
    return "\n".join(parts) + "\n" + hashtags
