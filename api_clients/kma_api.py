import requests
import json
import datetime

def get_weather_forecast(api_key, base_date, base_time, nx, ny):
    """기상청 단기예보 API를 호출하여 원시 데이터를 반환합니다."""
    weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    params = {
        "serviceKey": api_key,
        "numOfRows": 1000,
        "pageNo": 1,
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny,
        "dataType": "json"
    }

    try:
        response = requests.get(weather_url, params=params, timeout=10)
        print(f"Requesting Forecast URL: {response.url}") # Debug print
        response.raise_for_status()
        
        if response.status_code == 200 and response.text.strip():
            print("Requesting KMA API...")
            data = response.json()
            # print(f"Forecast API Response Data: {data}") # Debug print
            return data
        else:
            print(f"❌ 기상청 API 응답 오류 (상태 코드: {response.status_code})")
            return None

    except requests.exceptions.Timeout:
        print("❌ 기상청 API 호출 시간 초과 오류.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ 기상청 API 호출 오류: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ 기상청 API JSON 파싱 오류: {e}")
        return None


def get_weather_warnings(api_key, target_date):
    """
    기상청 기상속보 현황 API(getPwnStatus)를 호출하여 특정 지역에 '현재' 발효 중인 특보를 가져옵니다.
    
    Args:
        api_key (str): 공공데이터포털에서 발급받은 서비스 키
        target_date (str): 조회 기준 날짜 (API 호출 시 직접 사용되지는 않음)
        
    Returns:
        dict or None: API 응답 데이터를 JSON 형식으로 반환하거나, 오류 발생 시 None을 반환합니다.
    """
    warning_url = "http://apis.data.go.kr/1360000/WthrWrnInfoService/getPwnStatus"
    params = {
        "serviceKey": api_key,
        "pageNo": 1,
        "numOfRows": 10,
        "dataType": "JSON",
        "stnId": "109"  # 109: 서울
    }

    try:
        response = requests.get(warning_url, params=params, timeout=10)
        print(f"[DEBUG] Requesting Warnings URL: {response.url}") # 디버깅용 URL 출력
        response.raise_for_status()  # 200이 아닌 상태 코드에 대해 예외 발생

        if response.status_code == 200 and response.text.strip():
            print("기상특보 API 호출 성공")
            data = response.json()
            print(f"[DEBUG] Raw Warning API Response: {json.dumps(data, indent=2, ensure_ascii=False)}") # 디버깅용 원본 데이터 출력
            
            if not data.get('response', {}).get('body', {}).get('items', {}).get('item'):
                print(" -> 해당 지역에 발효된 기상특보가 없습니다.")
            
            return data
        else:
            print(f"❌ 기상특보 API 응답 오류 (상태 코드: {response.status_code})")
            return None

    except requests.exceptions.Timeout:
        print("❌ 기상특보 API 호출 시간 초과 오류.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ 기상특보 API 호출 오류: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ 기상특보 API JSON 파싱 오류: {e}")
        return None
