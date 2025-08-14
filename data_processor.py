# data_processor.py
# Processes raw data from APIs into meaningful information.
# 원시 API 데이터를 파싱하여 분석 가능한 형태로 변환합니다.

import xml.etree.ElementTree as ET

def process_weather_data(weather_api_data, target_date):
    """
    기상청 날씨 예보 API 데이터를 처리합니다.
    
    Args:
        weather_api_data: 기상청 API 원시 응답 데이터
        target_date: 처리할 날짜 (YYYYMMDD 형식)
    
    Returns:
        dict: 시간별 날씨 데이터가 정리된 딕셔너리
    """
    
    # 입력 데이터 유효성 검사
    if not weather_api_data or 'response' not in weather_api_data or 'body' not in weather_api_data['response']:
        print("❌ Invalid weather data.")
        return {}

    # 해당 날짜의 예보 항목만 필터링
    forecast_items = weather_api_data['response']['body']['items'].get('item', [])
    target_items = [item for item in forecast_items if item.get("fcstDate") == target_date]
    print(f" -> Processing {len(target_items)} items for target date ({target_date})...")

    # 결과 데이터 구조 초기화
    processed = {
        "temperatures": [],
        "humidity": [],
        "wind_speeds": [],
        "rain_prob": {},
        "rain_amount": {},
        "rain_amounts_list": [],
        "rain_type": {},
        "sky_status": {},
        "temp_max": None,
        "temp_min": None
    }
    
    # 각 예보 항목 처리
    for item in target_items:
        category = item["category"]
        value = item["fcstValue"]
        fcst_time = int(item["fcstTime"])

        try:
            if category == "TMP":
                processed["temperatures"].append({"time": fcst_time, "value": float(value)})
            elif category == "TMX":
                processed["temp_max"] = float(value)
            elif category == "TMN":
                processed["temp_min"] = float(value)
            elif category == "POP":
                processed["rain_prob"][fcst_time] = int(value)
            elif category == "PCP":
                # "강수없음"은 일반적으로 0mm를 의미하므로, 강수확률이 있을 경우를 대비해 0으로 처리
                if "강수없음" in value or "없음" in value:
                    amount = 0.0
                else:
                    # "mm" 단위 제거 및 공백 제거
                    value = value.replace("mm", "").strip()
                    try:
                        # "1.0 미만" 과 같은 형태 처리
                        if "미만" in value:
                            num_part = value.split(' ')[0]
                            amount = float(num_part) / 2 # 예: 1.0 미만 -> 0.5
                        # "5.0~10.0" 과 같은 범위 형태 처리
                        elif '~' in value:
                            parts = value.split('~')
                            amount = (float(parts[0]) + float(parts[1])) / 2
                        # 단일 숫자 값 처리
                        else:
                            amount = float(value)
                    except (ValueError, IndexError) as e:
                        print(f"⚠️ 강수량 파싱 오류 - 원본 값: '{item['fcstValue']}', 처리된 값: '{value}', 오류: {e}")
                        continue
                
                processed["rain_amount"][fcst_time] = amount
                processed["rain_amounts_list"].append(amount)

            elif category == "PTY":
                processed["rain_type"][fcst_time] = int(value)
            elif category == "REH":
                processed["humidity"].append({"time": fcst_time, "value": int(value)})
            elif category == "WSD":
                processed["wind_speeds"].append({"time": fcst_time, "value": float(value)})
            elif category == "SKY":
                processed["sky_status"][fcst_time] = int(value)
        except (ValueError, TypeError) as e:
            print(f"⚠️ Data processing error - Category: {category}, Value: {value}, Error: {e}")
            continue

    # TMX/TMN 값이 없는 경우, 시간별 온도 데이터에서 직접 계산
    if processed["temp_max"] is None and processed["temperatures"]:
        processed["temp_max"] = max(t['value'] for t in processed["temperatures"])
    if processed["temp_min"] is None and processed["temperatures"]:
        processed["temp_min"] = min(t['value'] for t in processed["temperatures"])

    # 처리 결과 요약 출력
    print(f" -> 온도 데이터: {len(processed['temperatures'])}개")
    print(f" -> 최고/최저온도: {processed['temp_max']}°C / {processed['temp_min']}°C")
    print(f" -> 강수확률 시간대: {len(processed['rain_prob'])}개")
    
    return processed

def extract_max_temp(processed_data):
    """
    처리된 데이터에서 최고온도만 추출합니다.
    TMX 값이 없으면 시간별 온도 중 최댓값을 사용합니다.
    
    Args:
        processed_data: process_weather_data()의 결과
    
    Returns:
        float: 최고온도 (°C) 또는 None
    """
    # TMX 값이 있으면 우선 사용
    if processed_data.get('temp_max') is not None:
        return processed_data['temp_max']
    
    # TMX가 없으면 시간별 온도 중 최댓값 계산
    temps = [t['value'] for t in processed_data.get('temperatures', [])]
    return max(temps) if temps else None

def process_uv_index(uv_api_data):
    """
    자외선 지수 API 데이터를 처리합니다.
    
    Args:
        uv_api_data: 자외선 지수 API 응답 데이터
    
    Returns:
        int: 최대 자외선 지수 또는 None
    """
    if not uv_api_data: 
        return None
        
    try:
        items = uv_api_data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
        if items:
            # h0, h3, h6, ... h24 형태의 시간별 UV 지수에서 최댓값 추출
            uv_values = []
            for i in range(0, 25, 3):  # 0, 3, 6, 9, 12, 15, 18, 21, 24시
                hour_key = f"h{i}"
                if items[0].get(hour_key, "").isdigit():
                    uv_values.append(int(items[0][hour_key]))
            
            return max(uv_values) if uv_values else None
            
    except (ValueError, TypeError, KeyError) as e:
        print(f"❌ UV index data processing error: {e}")
    
    return None

def process_air_forecast(air_forecast_data, pollutant_type='PM10'):
    """
    에어코리아 미세먼지/초미세먼지 예보 API 데이터를 처리하여 서울 지역의 예보 등급을 반환합니다.

    Args:
        air_forecast_data: 에어코리아 API 원시 응답 데이터
        pollutant_type (str): 처리할 오염물질 종류 ('PM10' 또는 'PM25')

    Returns:
        dict: {'status': 'Good', 'emoji': '🟢'} 형태의 딕셔너리.
              데이터가 없으면 N/A를 포함한 딕셔너리를 반환합니다.
    """
    if not air_forecast_data or 'response' not in air_forecast_data or 'body' not in air_forecast_data['response']:
        print(f"❌ 유효하지 않은 {pollutant_type} 대기질 예보 데이터입니다.")
        return {'status': 'N/A', 'emoji': '⚪'}

    items = air_forecast_data['response']['body'].get('items', [])
    if not items:
        return {'status': 'N/A', 'emoji': '⚪'}

    # informGrade 필드에 예보 등급이 들어있음 (예: "서울 : 좋음,제주 : 좋음,...")
    today_forecast = items[0].get('informGrade', '')
    seoul_grade = ''

    # 문자열에서 '서울' 지역의 등급만 파싱
    try:
        for part in today_forecast.split(','):
            if '서울' in part:
                seoul_grade = part.split(':')[1].strip()
                break
    except IndexError:
        print(f"❌ {pollutant_type} 대기질 예보 등급 파싱에 실패했습니다.")
        return {'status': 'N/A', 'emoji': '⚪'}

    if not seoul_grade:
        print(f"⚠️ 서울 지역의 {pollutant_type} 대기질 예보를 찾을 수 없습니다.")
        return {'status': 'N/A', 'emoji': '⚪'}

    print(f" -> 오늘 서울 {pollutant_type} 예보 등급: {seoul_grade}")

    # 등급에 따라 상태명과 이모지 결정
    if seoul_grade == '좋음':
        return {'status': 'Good', 'emoji': '🟢'}
    elif seoul_grade == '보통':
        return {'status': 'Moderate', 'emoji': '🟡'}
    elif seoul_grade == '나쁨':
        return {'status': 'Bad', 'emoji': '🔴'}
    elif seoul_grade == '매우나쁨':
        return {'status': 'Very Bad', 'emoji': '🟣'}
    else:
        return {'status': seoul_grade, 'emoji': '⚪'}





# process_astro_info 함수 제거 - astro_processor.py 사용

def process_weather_warnings(warning_api_data):
    """
    기상특보 API 데이터를 처리하여 현재 발효 중인 가장 중요한 특보 하나를 반환합니다.
    서울 지역(stnId=109)을 기준으로 하며, 우선순위는 태풍 > 폭염 > 호우 순입니다.
    getPwnStatus API의 응답 구조에 맞춰 t6 필드를 파싱합니다.

    Args:
        warning_api_data: 기상특보 API 원시 응답 데이터

    Returns:
        dict or None: 가장 우선순위가 높은 특보 정보 딕셔너리.
                      예: {'type': '폭염', 'level': '경보'}
                      처리할 특보가 없으면 None을 반환합니다.
    """
    if not warning_api_data or 'response' not in warning_api_data or 'body' not in warning_api_data['response']:
        print("❌ 유효하지 않은 특보 데이터입니다.")
        return None

    items = warning_api_data['response']['body'].get('items', {}).get('item', [])
    if not items:
        return None

    # 처리할 특보와 우선순위 정의 (낮을수록 우선순위 높음)
    priority_warnings = {
        '태풍': 1, '호우': 2, '폭염': 3, # 템플릿이 바뀌는 최우선 특보
        '한파': 4, '대설': 5, '강풍': 6, '건조': 7 # 말뭉치로 처리할 특보
    }
    detected_warnings = []

    for item in items:
        # getPwnStatus API의 특보 내용은 't6' 필드에 있음
        warning_content = item.get('t6', '')
        
        # API 응답에서 각 특보는 줄바꿈(\r\n 또는 \n)으로 구분될 수 있음
        # 일관된 처리를 위해 \r\n을 \n으로 통일하고, \n을 기준으로 나눔
        warning_lines = warning_content.replace('\r\n', '\n').split('\n')
        
        for line in warning_lines:
            # 라인 앞뒤의 공백 제거 후 내용이 있는지 확인
            line = line.strip()
            if '서울' in line and line:
                for key, priority in priority_warnings.items():
                    if key in line:
                        level = '알수없음'
                        if '경보' in line:
                            level = '경보'
                        elif '주의보' in line:
                            level = '주의보'
                        
                        detected_warnings.append({'type': key, 'level': level, 'priority': priority})
                        # 한 라인에서는 하나의 특보만 감지되면 되므로 break
                        break 
    
    if not detected_warnings:
        return None

    # 감지된 모든 서울 특보 중 우선순위가 가장 높은 것을 선택
    best_warning = min(detected_warnings, key=lambda x: x['priority'])
    
    # 최종 결과에서 priority 키는 제거하여 반환
    del best_warning['priority']

    print(f" -> 최종 선택된 기상특보: {best_warning}")
    return best_warning
