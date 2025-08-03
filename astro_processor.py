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

                # 월몰이 '----'일 경우 다음 날 월몰 정보 조회
                if result["moonset"] == "----":