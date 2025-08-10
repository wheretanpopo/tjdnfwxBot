# astro_processor.py
import xml.etree.ElementTree as ET
import datetime
from api_clients.kasi_api import get_astronomical_info, get_moon_phase_info

def classify_moon_phase(lun_age):
    """
    월령(lunAge)을 기반으로 달의 위상을 상세하게 분류합니다.
    천문학적 기준(29.53일 주기)을 적용하여 정확도를 높였습니다.

    Args:
        lun_age (float): API로부터 받은 월령 값.

    Returns:
        str: 상세 분류된 한글 달 위상 이름.
    """
    if not isinstance(lun_age, (int, float)):
        return "알 수 없음"

    # 월령 주기를 29.53일로 설정하고 각 위상 단계를 정의
    if 0 <= lun_age < 1.5:
        return "삭(그믐)"
    elif 1.5 <= lun_age < 7.38:
        return "초승달"
    elif 7.38 <= lun_age < 8.5:
        return "상현달"
    elif 8.5 <= lun_age < 14.76:
        return "상현망간"  # 보름달로 차오르는 달
    elif 14.76 <= lun_age <= 16.0:
        return "보름달"
    elif 16.0 < lun_age < 22.14:
        return "하현망간"  # 그믐달로 기우는 달
    elif 22.14 <= lun_age < 23.5:
        return "하현달"
    elif 23.5 <= lun_age < 29.53:
        return "그믐달"
    else:
        return "삭(그믐)"

def get_complete_astro_info(api_key, target_date, location="서울"):
    """
    지정한 날짜와 위치의 천문 정보를 통합하여 가져옵니다.
    일출/일몰, 월출/월몰, 낮/밤 길이, 달의 위상 정보를 모두 계산하여 반환합니다.

    Args:
        api_key (str): KASI API 키.
        target_date (datetime.date): 조회할 날짜.
        location (str): 조회할 지역.

    Returns:
        dict: 모든 천문 정보가 포함된 딕셔너리.
    """
    print(f"--- 천문 정보 조회 시작 (날짜: {target_date}, 지역: {location}) ---")

    # 1. KASI API를 통해 일출/일몰 및 월출/월몰 정보 조회
    sun_moon_xml = get_astronomical_info(api_key, location, target_date)
    
    # 2. KASI API를 통해 월령 정보 조회
    moon_phase_xml = get_moon_phase_info(api_key, target_date)
    
    # 결과를 저장할 기본 딕셔너리 구조
    result = {
        "sunrise": "N/A", "sunset": "N/A", 
        "moonrise": "N/A", "moonset": "N/A",
        "daylight_duration": "N/A", "night_duration": "N/A",
        "moon_age": None,
        "moon_phase_simple": "N/A",    # 영문 위상
        "moon_phase_ko": "N/A",        # 한글 위상
        "moon_emoji": "🌑"             # 달 이모지 (기본값 설정)
    }

    # 3. 일출/일몰, 월출/월몰 정보 처리
    if sun_moon_xml:
        try:
            root = ET.fromstring(sun_moon_xml)
            item = root.find(".//item")
            if item:
                result["sunrise"] = item.findtext("sunrise", "N/A").strip()
                result["sunset"] = item.findtext("sunset", "N/A").strip()
                result["moonrise"] = item.findtext("moonrise", "N/A").strip()
                result["moonset"] = item.findtext("moonset", "N/A").strip()
                print(f" → 일출/월몰 정보: {result['sunrise']}/{result['sunset']}, {result['moonrise']}/{result['moonset']}")

                # [오류 수정] 월몰 시간이 '----' (뜨지 않음)일 경우, 다음 날 월몰 시간 조회
                if result["moonset"] == "----":
                    print(" → 월몰 시간이 없어, 다음 날 월몰 시간을 조회합니다.")
                    next_day = target_date + datetime.timedelta(days=1)
                    next_day_sun_moon_xml = get_astronomical_info(api_key, location, next_day)
                    if next_day_sun_moon_xml:
                        next_day_root = ET.fromstring(next_day_sun_moon_xml)
                        next_day_item = next_day_root.find(".//item")
                        if next_day_item:
                            moonset_next_day = next_day_item.findtext("moonset", "----").strip()
                            if moonset_next_day != "----":
                                result["moonset"] = f"다음 날 {moonset_next_day}"
                                print(f" → 다음 날 월몰 시간 확인: {result['moonset']}")

                # [기능 복원] 낮과 밤 길이 계산
                if result["sunrise"] != "N/A" and result["sunset"] != "N/A":
                    try:
                        # 시간 형식 변환 (HHMM -> HH:MM)
                        sunrise_formatted = f"{result['sunrise'][:2]}:{result['sunrise'][2:]}"
                        sunset_formatted = f"{result['sunset'][:2]}:{result['sunset'][2:]}"

                        sunrise_time = datetime.datetime.strptime(sunrise_formatted, "%H:%M")
                        sunset_time = datetime.datetime.strptime(sunset_formatted, "%H:%M")
                        daylight = sunset_time - sunrise_time
                        
                        daylight_hours = daylight.seconds // 3600
                        daylight_minutes = (daylight.seconds % 3600) // 60
                        result["daylight_duration"] = f"{daylight_hours}h {daylight_minutes}m"
                        
                        night_duration_seconds = 24 * 3600 - daylight.seconds
                        night_hours = night_duration_seconds // 3600
                        night_minutes = (night_duration_seconds % 3600) // 60
                        result["night_duration"] = f"{night_hours}h {night_minutes}m"
                        print(f" → 낮/밤 길이 계산 완료: {result['daylight_duration']} / {result['night_duration']}")
                    except ValueError:
                        print("⚠️ 경고: 일출/일몰 시간 형식이 잘못되어 낮/밤 길이 계산에 실패했습니다.")
                        result["daylight_duration"] = "계산 불가"
                        result["night_duration"] = "계산 불가"

        except ET.ParseError as e:
            print(f"❌ 오류: 일출/월몰 정보 XML 파싱에 실패했습니다. {e}")

    # 4. 월령 정보 처리
    if moon_phase_xml:
        try:
            root = ET.fromstring(moon_phase_xml)
            item = root.find(".//item")
            if item:
                lun_age_str = item.findtext("lunAge", "0").strip()
                result["moon_age"] = float(lun_age_str)
                print(f" → 월령 정보 확인: {result['moon_age']}")
                
                # [기능 복원] 월령에 따른 상세 정보 분류
                result["moon_phase_ko"] = classify_moon_phase(result['moon_age'])
                
                phase_map = {
                    "초승달": ("Waxing Crescent", "🌒"),
                    "상현달": ("First Quarter", "🌓"),
                    "상현망간": ("Waxing Gibbous", "🌔"),
                    "보름달": ("Full Moon", "🌕"),
                    "하현망간": ("Waning Gibbous", "🌖"),
                    "하현달": ("Last Quarter", "🌗"),
                    "그믐달": ("Waning Crescent", "🌘"),
                    "삭(그믐)": ("New Moon", "🌑")
                }
                
                # 한글 위상에 매칭되는 영문 위상과 이모지 할당
                for key, values in phase_map.items():
                    if key in result["moon_phase_ko"]:
                        result["moon_phase_simple"], result["moon_emoji"] = values
                        break
                
                print(f" → 달 위상 분류 완료: {result['moon_phase_ko']} ({result['moon_phase_simple']}) {result['moon_emoji']}")

        except (ET.ParseError, ValueError) as e:
            print(f"❌ 오류: 월령 정보 XML 파싱 또는 값 변환에 실패했습니다. {e}")

    print("--- 천문 정보 조회 완료 ---")
    return result