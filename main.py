# main.py
# Main execution file for the weather service application.
# 매일 오전 5:30에 GitHub Actions로 실행되어 당일 날씨 정보를 수집하고 이미지를 생성합니다.

import datetime
import json
import subprocess # git 명령 실행을 위해 추가
from pathlib import Path
from zoneinfo import ZoneInfo # 시간대 정보 라이브러리

# 설정 및 API 클라이언트 모듈 임포트
from config import (
    KMA_API_KEY, AIRKOREA_API_KEY, KASI_API_KEY, 
    SEOUL_NX, SEOUL_NY, SEOUL_AREA_ID,
    INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_USER_ID, IMGUR_CLIENT_ID
)
from api_clients import kma_api, kasi_api, airkorea_api
from data_processor import (
    process_weather_data, 
    process_uv_index, 
    process_air_forecast, 
    process_weather_warnings
)
from forecast_generator import (
    analyze_processed_data, 
    create_instagram_summary
)
from astro_processor import get_complete_astro_info
from image_generator import ImageGenerator
from weather_phrases import WeatherPhraseGenerator
from weather_phrases_ko import WeatherPhraseGenerator as WeatherPhraseGeneratorKo
from outdoor_activity_index import calculate_activity_index
from instagram_api import InstagramAPI, post_daily_weather

# main.py 파일의 위치를 기준으로 상대 경로 설정
BASE_DIR = Path(__file__).parent
LAST_DAY_DATA_FILE = BASE_DIR / "weather_service" / "config" / "last_day_data.json"

def get_base_datetime():
    """
    KMA API 호출을 위한 적절한 기준 날짜와 시간을 계산합니다.
    API 데이터 생성 지연(약 15분)을 고려하여 현재 시간에서 20분을 뺀 시간을 기준으로, 요청 가능한 가장 최신 시간을 결정합니다.
    """
    now = datetime.datetime.now(ZoneInfo("Asia/Seoul")) # 한국 시간 기준
    base_criteria_time = now - datetime.timedelta(minutes=20)
    available_hours = [2, 5, 8, 11, 14, 17, 20, 23]
    
    base_date = base_criteria_time.strftime('%Y%m%d')
    base_hour = None
    for hour in sorted(available_hours, reverse=True):
        if base_criteria_time.hour >= hour:
            base_hour = hour
            break
    
    if base_hour is None:
        yesterday = base_criteria_time - datetime.timedelta(days=1)
        base_date = yesterday.strftime('%Y%m%d')
        base_hour = 23

    base_time = f"{base_hour:02d}00"
    return base_date, base_time

def load_yesterday_temps():
    """
    last_day_data.json 파일에서 어제의 최고/최저 기온을 로드합니다.
    """
    if not LAST_DAY_DATA_FILE.exists():
        print("⚠️ last_day_data.json 파일이 없습니다.")
        return None
    try:
        with open(LAST_DAY_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"❌ last_day_data.json 로드 중 오류: {e}")
        return None

def save_today_temps(temps):
    """
    오늘의 최고/최저 기온을 last_day_data.json 파일에 저장합니다.
    """
    try:
        LAST_DAY_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LAST_DAY_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(temps, f, indent=2, ensure_ascii=False)
        print(f"✅ 오늘 기온(최고/최저)을 저장했습니다.")
    except Exception as e:
        print(f"❌ 오늘 기온 저장 중 오류: {e}")

def main():
    """
    메인 실행 함수
    """
    # 1. 날짜 및 시간 설정 (한국 시간 기준)
    kst = ZoneInfo("Asia/Seoul")
    base_date, base_time = get_base_datetime()
    target_date = datetime.datetime.now(kst).strftime("%Y%m%d")
    yesterday_temps = load_yesterday_temps() # 어제 최고/최저 기온 모두 로드
    
    print("="*50)
    print(f"Weather Service Started for {target_date}")
    print(f"Base Time: {base_date} {base_time}")
    print("="*50)

    # 2. API 데이터 수집
    print("1. 모든 API 요청 중...")
    raw_weather_data = kma_api.get_weather_forecast(KMA_API_KEY, base_date, base_time, SEOUL_NX, SEOUL_NY)
    raw_uv_data = kasi_api.get_uv_index(KASI_API_KEY, SEOUL_AREA_ID, target_date)
    raw_warning_data = kma_api.get_weather_warnings(KMA_API_KEY, target_date)
    search_date_for_air = f"{target_date[:4]}-{target_date[4:6]}-{target_date[6:]}"
    raw_air_forecast_pm10 = airkorea_api.get_air_forecast(AIRKOREA_API_KEY, search_date_for_air, inform_code='PM10')
    raw_air_forecast_pm25 = airkorea_api.get_air_forecast(AIRKOREA_API_KEY, search_date_for_air, inform_code='PM25')
    astro_info = get_complete_astro_info(KASI_API_KEY, target_date, "서울")
    print(" -> 모든 API 호출 완료.")

    # 3. 데이터 가공
    print("\n2. 원시 데이터 처리 중...")
    processed_today = process_weather_data(raw_weather_data, target_date)
    uv_index = process_uv_index(raw_uv_data)
    warnings = process_weather_warnings(raw_warning_data)
    air_quality_pm10 = process_air_forecast(raw_air_forecast_pm10, pollutant_type='PM10')
    air_quality_pm25 = process_air_forecast(raw_air_forecast_pm25, pollutant_type='PM25')
    print(" -> 데이터 처리 완료.")

    # 4. 최종 분석
    print("\n3. 최종 데이터 분석 및 구축 중...")
    
    # 날짜 문자열로부터 날짜 객체 생성
    date_obj = datetime.datetime.strptime(target_date, "%Y%m%d")

    # 5. 공통 계산 (루프 밖에서 한 번만 계산)
    print("\n4. 공통 데이터 계산 중...")
    
    # PM10, PM2.5 중 더 나쁜 등급을 기준으로 air_quality를 정함
    pm10_status = air_quality_pm10.get('status', 'N/A')
    pm25_status = air_quality_pm25.get('status', 'N/A')
    status_priority = {"Very Bad": 4, "Bad": 3, "Moderate": 2, "Good": 1, "N/A": 0}
    main_air_quality = pm10_status if status_priority.get(pm10_status, 0) >= status_priority.get(pm25_status, 0) else pm25_status

    # 안전한 기본값 설정 (원시 데이터에서 직접 계산)
    temps = [t['value'] for t in processed_today.get('temperatures', [])]
    daily_max_temp = processed_today.get('temp_max') or (max(temps) if temps else 20)
    daily_uv_max = uv_index if uv_index and uv_index != 'N/A' else 5  # 기본값 5

    print(f" -> 일최고기온: {daily_max_temp}°C, UV지수: {daily_uv_max}, 주요대기질: {main_air_quality}")

    # 6. 기본 데이터 구조 생성
    base_final_data = {
        "info": {
            "target_date": target_date,
            "date_object": date_obj
        },
        "indices": {
            "uv_index": uv_index,
            "air_quality_pm10": air_quality_pm10,
            "air_quality_pm25": air_quality_pm25,
        },
        "astro_info": astro_info,
        "warnings": warnings
    }
    print(" -> 기본 데이터 구조 생성 완료.")

    # 7. 언어별 이미지 생성
    print("\n5. 언어별 이미지 생성 중...")
    languages = ['en', 'ko']
    generated_images = {}
    lang_data = {}  # 캐치프레이즈 등 언어별 데이터 저장

    for lang in languages:
        print(f"\n--- {lang.upper()} 버전 생성 시작 ---")
        
        # 언어별 날씨 요약 생성
        weather_summary = analyze_processed_data(processed_today, target_date, yesterday_temps, warnings, language=lang)
        
        # 언어별 캐치프레이즈 생성기 선택
        if lang == 'ko':
            phrase_gen = WeatherPhraseGeneratorKo()
        else:
            phrase_gen = WeatherPhraseGenerator()

        # 언어별 최종 데이터 생성 (기본 데이터에 weather_summary 추가)
        final_data = base_final_data.copy()
        final_data['indices'] = base_final_data['indices'].copy()  # 깊은 복사
        final_data['weather_summary'] = weather_summary

        # 캐치프레이즈 생성
        catch_phrase = phrase_gen.generate_phrase(final_data)
        print(f" -> 오늘의 캐치프레이즈 ({lang}): {catch_phrase}")

        # 언어별 데이터 저장
        lang_data[lang] = {
            'catch_phrase': catch_phrase,
            'weather_summary': weather_summary
        }

        # 야외활동 지수 계산 (언어별)
        print(f" -> 야외활동 지수 계산 중 ({lang})...")
        index_am = calculate_activity_index(processed_today, 'am', daily_max_temp, daily_uv_max, main_air_quality, language=lang)
        index_pm = calculate_activity_index(processed_today, 'pm', daily_max_temp, daily_uv_max, main_air_quality, language=lang)
        print(f" -> 오전 지수: {index_am['grade']}")
        print(f" -> 오후 지수: {index_pm['grade']}")

        # 활동 지수를 최종 데이터에 추가
        final_data['indices']['activity_index_am'] = index_am
        final_data['indices']['activity_index_pm'] = index_pm

        # 이미지 생성
        img_gen = ImageGenerator()
        img_gen.setup()
        image_path, _ = img_gen.create_post_image(final_data, catch_phrase, index_am, index_pm, language=lang)
        
        if image_path:
            generated_images[lang] = image_path
            print(f" -> {lang.upper()} 이미지 생성 완료: {image_path}")

            # 한국어 포스트 이미지가 생성되면, 바로 스토리용 이미지도 생성
            if lang == 'ko':
                story_image_path = img_gen.create_story_from_post(image_path)
                if story_image_path:
                    generated_images['story_ko'] = story_image_path
        else:
            print(f" -> ❌ {lang.upper()} 이미지 생성 실패")

    # 8. Instagram 포스팅
    print(f"\n6. Instagram 포스팅 시작...")
    
    if not generated_images:
        print("❌ 생성된 이미지가 없어 Instagram 포스팅을 건너뜁니다.")
    else:
        print(f"   생성된 이미지: {list(generated_images.keys())}")
        
        # Instagram API 인스턴스 생성
        if all([INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_USER_ID, IMGUR_CLIENT_ID]):
            instagram_api = InstagramAPI(INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_USER_ID, IMGUR_CLIENT_ID)
            
            # 일일 날씨 포스팅 실행
            posting_success = post_daily_weather(instagram_api, generated_images, lang_data)
            
            if posting_success:
                print("✅ Instagram 포스팅 완료!")
            else:
                print("❌ Instagram 포스팅 중 일부 실패")
        else:
            print("❌ Instagram API 설정이 부족합니다. 포스팅을 건너뜁니다.")
            print(f"   - ACCESS_TOKEN: {'✅' if INSTAGRAM_ACCESS_TOKEN else '❌'}")
            print(f"   - USER_ID: {'✅' if INSTAGRAM_USER_ID else '❌'}")
            print(f"   - IMGUR_CLIENT_ID: {'✅' if IMGUR_CLIENT_ID else '❌'}")

    # 9. 오늘 최고/최저 기온 저장 (원시 데이터에서 직접 계산)
    print(f"\n7. 데이터 저장 중...")
    temps = [t['value'] for t in processed_today.get('temperatures', [])]
    temp_max_for_save = processed_today.get('temp_max') or (max(temps) if temps else None)
    temp_min_for_save = processed_today.get('temp_min') or (min(temps) if temps else None)
    
    today_temps_to_save = {
        'yesterday_max_temp': temp_max_for_save,
        'yesterday_min_temp': temp_min_for_save
    }
    print(f"[DEBUG] today_temps_to_save: {today_temps_to_save}") # 디버그 출력 추가
    if today_temps_to_save['yesterday_max_temp'] is not None:
        save_today_temps(today_temps_to_save)
        print(f"[DEBUG] last_day_data.json content after save: {load_yesterday_temps()}") # 디버그 출력 추가
        
        # --- Git에 변경사항 커밋 및 푸시 ---
        print("\n8. 변경된 기온 데이터 Git에 저장 중...")
        try:
            # 1. Git 사용자 설정
            subprocess.run(['git', 'config', '--global', 'user.name', 'github-actions[bot]'], check=True)
            subprocess.run(['git', 'config', '--global', 'user.email', 'github-actions[bot]@users.noreply.github.com'], check=True)
            
            # 2. 파일 스테이징
            subprocess.run(['git', 'add', str(LAST_DAY_DATA_FILE)], check=True)
            
            # 3. 변경사항 확인 및 커밋
            status_result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
            print(f"[DEBUG] git status --porcelain output: {status_result.stdout}") # 디버그 출력 추가
            # 파일 경로를 상대 경로로 변환하고 슬래시를 통일하여 비교
            file_path_for_git_status = str(LAST_DAY_DATA_FILE.relative_to(BASE_DIR)).replace('\\', '/')
            # 'M  ' (modified, staged) 상태로 파일이 있는지 확인
            if f"M  {file_path_for_git_status}" in status_result.stdout:
                commit_message = f"[BOT] Update temperature data for {target_date}"
                subprocess.run(['git', 'commit', '-m', commit_message], check=True)
                print(f" -> 커밋 생성: {commit_message}")
                
                # 4. 푸시
                subprocess.run(['git', 'push', 'origin', 'main'], check=True) # 'origin main' 명시적으로 지정
                print(" -> Git 저장소에 성공적으로 푸시했습니다.")
            else:
                print(" -> 변경사항이 없어 커밋을 건너뜁니다.")

        except subprocess.CalledProcessError as e:
            print(f"❌ Git 작업 실패: {e}")
        except Exception as e:
            print(f"❌ 예상치 못한 오류 발생: {e}")
    
    print("\n" + "="*50)
    print("Weather Service Completed Successfully! 🎉")
    print("="*50)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred during main execution: {e}")
        import traceback
        traceback.print_exc()
        raise
