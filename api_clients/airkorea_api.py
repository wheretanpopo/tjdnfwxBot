# api_clients/airkorea_api.py
# 한국환경공단 에어코리아 API 관련 함수들을 관리합니다.

import requests
import json

def get_air_forecast(api_key, search_date, inform_code="PM10"):
    """
    한국환경공단 에어코리아의 '미세먼지 예보통보 조회' API를 호출합니다.
    요청된 inform_code에 따라 예보를 가져옵니다.

    Args:
        api_key (str): 공공데이터포털 서비스 키
        search_date (str): 조회할 날짜 (YYYY-MM-DD 형식)
        inform_code (str): 요청할 코드 ('PM10' 또는 'PM25')

    Returns:
        dict or None: API 응답 데이터를 JSON 형식으로 반환하거나, 오류 발생 시 None을 반환합니다.
    """
    api_url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMinuDustFrcstDspth"
    params = {
        "serviceKey": api_key,
        "returnType": "json",
        "numOfRows": 10,
        "pageNo": 1,
        "searchDate": search_date,
        "informCode": inform_code
    }

    try:
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()

        if response.status_code == 200 and response.text.strip():
            print(f"에어코리아 {inform_code} 예보 API 호출 성공")
            return response.json()
        else:
            print(f"❌ 에어코리아 {inform_code} 예보 API 응답 오류 (상태 코드: {response.status_code})")
            return None

    except requests.exceptions.Timeout:
        print(f"❌ 에어코리아 {inform_code} 예보 API 호출 시간 초과 오류.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ 에어코리아 {inform_code} 예보 API 호출 오류: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ 에어코리아 {inform_code} 예보 API JSON 파싱 오류: {e}")
        return None
