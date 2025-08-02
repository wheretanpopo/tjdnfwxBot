# instagram_api.py
# Instagram API 연동 및 포스팅 기능
# 캐러셀, 스토리 포스팅 등을 담당합니다.

import requests
import datetime
from zoneinfo import ZoneInfo # 시간대 정보 라이브러리
from imgurpython import ImgurClient
from pathlib import Path

class InstagramAPI:
    def __init__(self, access_token, user_id, imgur_client_id):
        self.access_token = access_token
        self.user_id = user_id
        self.imgur_client_id = imgur_client_id
        self.base_url = "https://graph.facebook.com/v20.0"
        
    def upload_to_imgur(self, image_path):
        """
        이미지를 Imgur에 업로드하고 이미지 URL을 반환합니다.
        """
        print(f"-> Imgur에 이미지 업로드 시작: {image_path}")
        if not self.imgur_client_id:
            print("❌ Imgur 클라이언트 ID가 설정되지 않았습니다.")
            return None
        try:
            client = ImgurClient(self.imgur_client_id, None)
            uploaded_image = client.upload_from_path(str(image_path), config=None, anon=True)
            print(f"✅ Imgur 업로드 성공! URL: {uploaded_image['link']}")
            return uploaded_image['link']
        except Exception as e:
            print(f"❌ Imgur 업로드 실패: {e}")
            return None

    def create_media_container(self, image_url, caption, is_carousel_item=False):
        """
        Instagram 미디어 컨테이너를 생성합니다.
        """
        url = f"{self.base_url}/{self.user_id}/media"
        params = {
            'image_url': image_url,
            'access_token': self.access_token
        }
        
        # 캐러셀 아이템이 아닌 경우에만 캡션 추가
        if not is_carousel_item:
            params['caption'] = caption
            
        try:
            response = requests.post(url, params=params)
            response.raise_for_status()
            result = response.json()
            
            if 'id' in result:
                print(f"✅ 미디어 컨테이너 생성 성공: {result['id']}")
                return result['id']
            else:
                print(f"❌ 미디어 컨테이너 생성 실패: {result}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 미디어 컨테이너 생성 실패: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"    - 응답 내용: {e.response.text}")
            return None

    def create_carousel_container(self, media_ids, caption):
        """
        캐러셀 컨테이너를 생성합니다.
        """
        url = f"{self.base_url}/{self.user_id}/media"
        params = {
            'media_type': 'CAROUSEL',
            'children': ','.join(media_ids),
            'caption': caption,
            'access_token': self.access_token
        }
        
        try:
            response = requests.post(url, params=params)
            print(f"요청 URL: {response.request.url}")
            print(f"요청 바디: {response.request.body}")
            print(f"응답 코드: {response.status_code}")
            print(f"응답 본문: {response.text}")
            response.raise_for_status()
            result = response.json()
            
            if 'id' in result:
                print(f"✅ 캐러셀 컨테이너 생성 성공: {result['id']}")
                return result['id']
            else:
                print(f"❌ 캐러셀 컨테이너 생성 실패: {result}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 캐러셀 컨테이너 생성 실패: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"    - 응답 내용: {e.response.text}")
            return None

    def publish_media(self, creation_id):
        """
        미디어를 Instagram에 게시합니다.
        """
        url = f"{self.base_url}/{self.user_id}/media_publish"
        params = {
            'creation_id': creation_id,
            'access_token': self.access_token
        }
        
        try:
            response = requests.post(url, params=params)
            response.raise_for_status()
            result = response.json()
            
            if 'id' in result:
                print(f"✅ 미디어 게시 성공! 포스트 ID: {result['id']}")
                return result['id']
            else:
                print(f"❌ 미디어 게시 실패: {result}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 미디어 게시 실패: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"    - 응답 내용: {e.response.text}")
            return None

    def post_single_image(self, image_path, caption):
        """
        단일 이미지를 Instagram에 포스팅합니다.
        """
        print(f"-> 단일 이미지 포스팅 시작: {image_path}")
        
        # 1. Imgur에 업로드
        image_url = self.upload_to_imgur(image_path)
        if not image_url:
            return None
            
        # 2. 미디어 컨테이너 생성
        creation_id = self.create_media_container(image_url, caption)
        if not creation_id:
            return None
            
        # 3. 게시
        post_id = self.publish_media(creation_id)
        return post_id

    def post_carousel(self, image_paths, caption):
        """
        여러 이미지를 캐러셀로 Instagram에 포스팅합니다.
        """
        print(f"-> 캐러셀 포스팅 시작: {len(image_paths)}개 이미지")
        
        if len(image_paths) < 2 or len(image_paths) > 10:
            print("❌ 캐러셀은 2~10개의 이미지가 필요합니다.")
            return None
            
        media_ids = []
        
        # 1. 각 이미지를 Imgur에 업로드하고 미디어 컨테이너 생성
        for i, image_path in enumerate(image_paths):
            print(f"   처리 중: {i+1}/{len(image_paths)} - {image_path}")
            
            # Imgur에 업로드
            image_url = self.upload_to_imgur(image_path)
            if not image_url:
                print(f"❌ {i+1}번째 이미지 업로드 실패")
                return None
                
            # 캐러셀 아이템용 미디어 컨테이너 생성 (캡션 없음)
            media_id = self.create_media_container(image_url, "", is_carousel_item=True)
            if not media_id:
                print(f"❌ {i+1}번째 미디어 컨테이너 생성 실패")
                return None
                
            media_ids.append(media_id)
        
        # 2. 캐러셀 컨테이너 생성
        carousel_id = self.create_carousel_container(media_ids, caption)
        if not carousel_id:
            return None
            
        # 3. 게시
        post_id = self.publish_media(carousel_id)
        return post_id

    def post_story(self, image_path):
        """
        이미지를 Instagram 스토리에 포스팅합니다.
        """
        print(f"-> 스토리 포스팅 시작: {image_path}")
        
        # 1. Imgur에 업로드
        image_url = self.upload_to_imgur(image_path)
        if not image_url:
            return None
            
        # 2. 스토리용 미디어 컨테이너 생성
        url = f"{self.base_url}/{self.user_id}/media"
        params = {
            'image_url': image_url,
            'media_type': 'STORIES',
            'access_token': self.access_token
        }
        
        try:
            response = requests.post(url, params=params)
            response.raise_for_status()
            result = response.json()
            
            if 'id' in result:
                creation_id = result['id']
                print(f"✅ 스토리 컨테이너 생성 성공: {creation_id}")
                
                # 3. 스토리 게시
                story_id = self.publish_media(creation_id)
                return story_id
            else:
                print(f"❌ 스토리 컨테이너 생성 실패: {result}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 스토리 포스팅 실패: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"    - 응답 내용: {e.response.text}")
            return None

    def create_caption_for_carousel(self, lang_data, primary_lang='ko'):
        """
        캐러셀용 캡션을 생성합니다.
        """
        # 주 언어의 캐치프레이즈를 메인으로 사용
        main_phrase = lang_data.get(primary_lang, {}).get('catch_phrase', 'Great weather today!')
        date_str = datetime.datetime.now(ZoneInfo("Asia/Seoul")).strftime('%B %d, %Y')
        
        # 기본 캡션 구성
        caption_parts = [
            f"📅 {date_str}",
            f"✨ {main_phrase}",
            "",
            "by Seoul Weather Forecast",
            "",
            "모든 날씨 정보는 매일 새벽 5시 30분 기준으로 생성됩니다.",
            "특히, 기상특보(폭염, 호우 등)는 이 시각에 발효 중인 내용을 반영하므로, 이후에 발표되거나 해제되는 특보와는 차이가 있을 수 있습니다.",
            "",
            "All weather information is generated daily at 5:30 AM.",
            "In particular, weather advisories/warnings (such as heat waves or heavy rain) reflect the status as of that time. Please note that any advisories issued or lifted after this time may not be reflected.",
            "",
            "#WeatherForecast #Seoul #DailyWeather",
            "#날씨예보 #서울날씨 #오늘의날씨 #서울",
            "#WeatherUpdate #KoreaWeather #Weather"
        ]
        
        return "\n".join(caption_parts)


def post_daily_weather(instagram_api, generated_images, lang_data):
    """
    일일 날씨 정보를 Instagram에 포스팅합니다.
    
    Args:
        instagram_api: InstagramAPI 인스턴스
        generated_images: {'ko': path, 'en': path} 형태의 딕셔너리
        lang_data: {'ko': {'catch_phrase': '...'}, 'en': {'catch_phrase': '...'}}
    """
    if not generated_images:
        print("❌ 생성된 이미지가 없습니다.")
        return False
        
    current_day = datetime.datetime.now(ZoneInfo("Asia/Seoul")).day
    
    # 홀수날: 한국어 우선, 짝수날: 영어 우선
    if current_day % 2 == 1:  # 홀수날
        post_order = ['ko', 'en']
        primary_lang = 'ko'
        print(f"📅 홀수날({current_day}일) - 한국어 우선 순서")
    else:  # 짝수날
        post_order = ['en', 'ko'] 
        primary_lang = 'en'
        print(f"📅 짝수날({current_day}일) - 영어 우선 순서")
    
    # 사용 가능한 이미지만 필터링
    available_images = [generated_images[lang] for lang in post_order if lang in generated_images and generated_images[lang]]
    
    if not available_images:
        print("❌ 사용할 수 있는 이미지가 없습니다.")
        return False
    
    success = True
    
    try:
        # 1. 캐러셀 포스팅 (영어/한국어 또는 단일 이미지)
        if len(available_images) >= 2:
            print(f"-> 캐러셀 포스팅 시작 (순서: {' → '.join(post_order)})")
            caption = instagram_api.create_caption_for_carousel(lang_data, primary_lang)
            carousel_result = instagram_api.post_carousel(available_images, caption)
            
            if carousel_result:
                print(f"✅ 캐러셀 포스팅 성공! ID: {carousel_result}")
            else:
                print("❌ 캐러셀 포스팅 실패")
                success = False
        else:
            print("-> 단일 이미지 포스팅")
            single_lang = post_order[0] if post_order[0] in generated_images else list(generated_images.keys())[0]
            caption = instagram_api.create_caption_for_carousel(lang_data, single_lang)
            single_result = instagram_api.post_single_image(available_images[0], caption)
            
            if single_result:
                print(f"✅ 단일 포스팅 성공! ID: {single_result}")
            else:
                print("❌ 단일 포스팅 실패")
                success = False
        
        # 2. 스토리 포스팅 (한국어 버전 우선)
        story_image_to_post = generated_images.get('story_ko') or generated_images.get('ko')
        if story_image_to_post:
            print(f"-> 스토리 포스팅 시작 ({'전용 이미지' if 'story_ko' in generated_images else '포스트 이미지 사용'})")
            story_result = instagram_api.post_story(story_image_to_post)
            
            if story_result:
                print(f"✅ 스토리 포스팅 성공! ID: {story_result}")
            else:
                print("❌ 스토리 포스팅 실패")
                success = False
        else:
            print("⚠️ 한국어 이미지가 없어 스토리 포스팅을 건너뜁니다.")
    
    except Exception as e:
        print(f"❌ Instagram 포스팅 중 오류 발생: {e}")
        success = False
    
    
    
    
    
    return success
