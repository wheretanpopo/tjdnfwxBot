# api_clients/kasi_api.py
# 한국천문연구원 생활지수 및 천문 정보 API 관련 함수들을 관리합니다.

import requests
import json
import xml.etree.ElementTree as ET

def get_uv_index(api_key, area_no, target_date):
    """자외선 지수 API를 호출합니다."""
    uv_url = "http://apis.data.go.kr/1360000/LivingWthrIdxServiceV4/getUVIdxV4"
    params = {
        "serviceKey": api_key,
        "areaNo": area_no,
        "time": f"{target_date}06",
        "dataType": "json"
    }
    try:
        response = requests.get(uv_url, params=params, timeout=10)
        response.raise_for_status()
        if response.status_code == 200 and response.text.strip():
            print("자외선 지수 API 호출 성공")
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ 자외선 지수 API 오류: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ 자외선 지수 JSON 파싱 오류: {e}")
    return None



def get_astronomical_info(api_key, location, target_date):
    """일출/일몰, 월출/월몰 정보를 XML 형식으로 가져옵니다."""
    url = "http://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getAreaRiseSetInfo"
    params = {"serviceKey": api_key, "location": location, "locdate": target_date}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        if response.status_code == 200 and response.text.strip():
            print("일출/일몰 API 호출 성공")
            return response.text
    except requests.exceptions.RequestException as e:
        print(f"❌ 일출/일몰 API 오류: {e}")
    return None

def get_moon_phase_info(api_key, target_date):
    """월령 정보를 XML 형식으로 가져옵니다."""
    url = "http://apis.data.go.kr/B090041/openapi/service/LunPhInfoService/getLunPhInfo"
    params = {
        "serviceKey": api_key,
        "solYear": target_date[:4],
        "solMonth": target_date[4:6],
        "solDay": target_date[6:]
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        if response.status_code == 200 and response.text.strip():
            print("월령 API 호출 성공")
            return response.text
    except requests.exceptions.RequestException as e:
        print(f"❌ 월령 API 오류: {e}")
    return None
