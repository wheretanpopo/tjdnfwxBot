# astro_processor.py
import xml.etree.ElementTree as ET
import datetime
from api_clients.kasi_api import get_astronomical_info, get_moon_phase_info

def classify_moon_phase(lun_age):
    """상세한 달 모양 분류 - 정확한 천문학적 기준 적용"""
    # 정확한 천문학적 기준: 29.53일 주기, 각 위상 약 7.38일
    if 0 <= lun_age < 1.5:
        return "삭 (그믐)"
    elif 1.5 <= lun_age < 7.38:  # 초승달 범위 확장 (기존 6.5 → 7.38)
        if 3.5 <= lun_age < 4.5:
            return "완전 초승달"
        else:
            return "초승달"
    elif 7.38 <= lun_age < 8.5:  # 상현달 시작점 조정
        if 7.5 <= lun_age < 8.0:
            return "완전 상현달"
        else:
            return "상현달"
    elif 8.5 <= lun_age < 14.76:  # 상현망간 범위 조정
        return "상현망간"
    elif 14.76 <= lun_age <= 16.0:  # 보름달 범위 조정
        if 14.6 <= lun_age <= 15.0:
            return "완전 보름달"
        else:
            return "보름달"
    elif 16.0 < lun_age < 22.14:  # 하현망간 범위 조정
        return "하현망간"
    elif 22.14 <= lun_age < 23.5:  # 하현달 시작점 조정
        if 22.1 <= lun_age < 22.5:
            return "완전 하현달"
        else:
            return "하현달"
    elif 23.5 <= lun_age < 29.53:  # 그믐달 범위 조정 (29.0 → 29.53)
        return "그믐달"
    else:
        return "삭 (그믐)"

def get_complete_astro_info(api_key, target_date, location="서울"):
    """천문 정보 통합 처리 - 다국어 지원 및 정확한 분류"""
    
    sun_moon_xml = get_astronomical_info(api_key, location, target_date)
    moon_phase_xml = get_moon_phase_info(api_key, target_date)
    
    result = {
        "sunrise": "N/A", "sunset": "N/A", 
        "moonrise": "N/A", "moonset": "N/A",
        "daylight_duration": "N/A", "night_duration": "N/A",
        "moon_age": None,
        "moon_phase_simple": "N/A",    # 영어 간단
        "moon_phase_ko": "N/A",        # 한국어 간단
        "moon_emoji": "🌑"
    }
    
    if sun_moon_xml:
        try:
            root = ET.fromstring(sun_moon_xml)
            item = root.find(".//item")
            if item:
                result["sunrise"] = item.findtext("sunrise", "N/A").strip()
                result["sunset"] = item.findtext("sunset", "N/A").strip()
                result["moonrise"] = item.findtext("moonrise", "N/A").strip()
                result["moonset"] = item.findtext("moonset", "N/A").strip()
                
                try:
                    sunrise_dt = datetime.datetime.strptime(result["sunrise"], "%H%M")
                    sunset_dt = datetime.datetime.strptime(result["sunset"], "%H%M")
                    daylight = sunset_dt - sunrise_dt
                    night = datetime.timedelta(hours=24) - daylight
                    result["daylight_duration"] = f"{int(daylight.total_seconds()//3600)}h {int((daylight.total_seconds()%3600)//60)}m"
                    result["night_duration"] = f"{int(night.total_seconds()//3600)}h {int((night.total_seconds()%3600)//60)}m"
                except: pass
        except ET.ParseError as e:
            print(f"Error parsing sun/moon XML: {e}")
    
    if moon_phase_xml:
        try:
            root = ET.fromstring(moon_phase_xml)
            age_elem = root.find(".//lunAge")
            if age_elem is not None:
                moon_age = float(age_elem.text)
                result["moon_age"] = moon_age
                
                # 영어/한국어/이모지 동시 분류
                if moon_age < 1.5: phase_en, phase_ko, emoji = "New Moon", "삭", "🌑"
                elif moon_age < 7.38: phase_en, phase_ko, emoji = "Waxing Crescent", "초승달", "🌒"
                elif moon_age < 8.5: phase_en, phase_ko, emoji = "First Quarter", "상현달", "🌓"
                elif moon_age < 14.76: phase_en, phase_ko, emoji = "Waxing Gibbous", "상현망간달", "🌔"
                elif moon_age <= 16.0: phase_en, phase_ko, emoji = "Full Moon", "보름달", "🌕"
                elif moon_age < 22.14: phase_en, phase_ko, emoji = "Waning Gibbous", "하현망간달", "🌖"
                elif moon_age < 23.5: phase_en, phase_ko, emoji = "Last Quarter", "하현달", "🌗"
                else: phase_en, phase_ko, emoji = "Waning Crescent", "그믐달", "🌘"
                
                result["moon_phase_simple"] = phase_en
                result["moon_phase_ko"] = phase_ko
                result["moon_emoji"] = emoji
                    
        except (ET.ParseError, ValueError) as e:
            print(f"Error processing moon phase data: {e}")
    
    return result

def test_astro_info_debug():
    """천문 정보 디버깅 테스트 - 기존 함수명 유지"""
    from config import KASI_API_KEY
    
    print("=== 천문 정보 디버깅 테스트 (개선된 분류) ===")
    
    tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y%m%d")
    print(f"📅 대상 날짜: {tomorrow}")
    print(f"🔑 API 키 길이: {len(KASI_API_KEY)}")
    
    # 1. API 호출 테스트
    print("\n1️⃣ 일출/일몰 API 호출 중...")
    sun_moon_xml = get_astronomical_info(KASI_API_KEY, "서울", tomorrow)
    if sun_moon_xml:
        print(f"✅ 일출/일몰 데이터 받음 (길이: {len(sun_moon_xml)})")
        print(f"📄 내용 미리보기: {sun_moon_xml[:200]}...")
    else:
        print("❌ 일출/일몰 데이터 없음")
    
    print("\n2️⃣ 월령 API 호출 중...")
    moon_phase_xml = get_moon_phase_info(KASI_API_KEY, tomorrow)
    if moon_phase_xml:
        print(f"✅ 월령 데이터 받음 (길이: {len(moon_phase_xml)})")
        print(f"📄 내용 미리보기: {moon_phase_xml[:200]}...")
    else:
        print("❌ 월령 데이터 없음")
    
    # 2. 통합 처리 테스트
    print("\n3️⃣ 데이터 통합 처리 중...")
    result = get_complete_astro_info(KASI_API_KEY, tomorrow)
    
    print("\n=== 📊 최종 결과 (개선된 분류) ===")
    for key, value in result.items():
        print(f"{key}: {value}")
    
    # 3. 이모지 특별 확인
    print(f"\n🌙 월령 이모지: {result['moon_emoji']}")
    print(f"📱 이모지 코드: {ord(result['moon_emoji'][0]) if result['moon_emoji'] else 'None'}")
    
    # 4. 개선점 확인 (새로 추가)
    print("\n=== 🔍 개선점 확인 ===")
    test_age = 7.0
    old_classification = "상현달" if test_age >= 6.5 else "초승달"  # 기존 기준
    new_classification = classify_moon_phase(test_age)  # 개선된 기준
    print(f"월령 {test_age}일:")
    print(f"  기존 분류: {old_classification}")
    print(f"  개선 분류: {new_classification}")
    print(f"  실제 관측: 초승달 ✅" if "초승달" in new_classification else "")
    
    print("\n=== 디버깅 테스트 완료 ===")

if __name__ == "__main__":
    test_astro_info_debug()