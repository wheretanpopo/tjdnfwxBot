# image_generator.py
# Generates Instagram images based on weather data.

import datetime
import json
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji

class ImageGenerator:
    """
    날씨 데이터 기반 Instagram 이미지 생성기
    """
    
    def __init__(self, base_dir_name="weather_service"):
        self.base_dir = Path("D:/Documents/Gemini_Projects/MyFirstGeminiApp") / base_dir_name
        self.templates_dir = self.base_dir / "templates"
        self.fonts_dir = self.base_dir / "fonts"
        self.config_dir = self.base_dir / "config"
        self.output_dir = self.base_dir / "output"
        
        # 폰트 경로 정의 (한국어 폰트도 영어와 동일하게 처리)
        self.font_paths = {
            'Bellota-Bold': self.fonts_dir / 'Bellota-Bold.ttf',
            'Bellota-Regular': self.fonts_dir / 'Bellota-Regular.ttf',
            'Inter_24pt-ExtraBold': self.fonts_dir / 'Inter_24pt-ExtraBold.ttf',
            'Inter_24pt-SemiBold': self.fonts_dir / 'Inter_24pt-SemiBold.ttf',
            'Inter_18pt-Regular': self.fonts_dir / 'Inter_18pt-Regular.ttf',
            'Satoshi-Bold': self.fonts_dir / 'Satoshi-Bold.ttf',
            'NotoColorEmoji-Regular': self.fonts_dir / 'NotoColorEmoji-Regular.ttf',
            # 한국어 폰트들 - 영어와 동일한 방식으로 처리
            'NanumSquareNeo-bRg': self.fonts_dir / 'NanumSquareNeo-bRg.ttf',
            'NanumSquareNeo-cBd': self.fonts_dir / 'NanumSquareNeo-cBd.ttf',
            'NanumSquareNeo-dEb': self.fonts_dir / 'NanumSquareNeo-dEb.ttf',
            'NanumSquareNeo-eHv': self.fonts_dir / 'NanumSquareNeo-eHv.ttf',
            'NanumGothic': self.fonts_dir / 'NanumGothic.ttf',
        }

    def load_positions(self):
        positions_path = self.config_dir / 'positions.json'
        try:
            with open(positions_path, 'r', encoding='utf-8') as f:
                self.positions = json.load(f)
                print("✅ positions.json 로드 완료")
        except FileNotFoundError:
            print(f"❌ positions.json을 찾을 수 없습니다: {positions_path}")
            self.positions = {}
        except json.JSONDecodeError:
            print(f"❌ positions.json JSON 디코딩 오류: {positions_path}")
            self.positions = {}

    def load_templates(self):
        """템플릿 로드 (현재는 파일 존재 여부만 확인)"""
        posts_dir = self.templates_dir / "posts"
        if posts_dir.exists():
            template_count = len(list(posts_dir.glob("*.png")))
            print(f"✅ 템플릿 디렉토리 확인 완료: {template_count}개 템플릿 발견")
        else:
            print(f"⚠️ 템플릿 디렉토리가 없습니다: {posts_dir}")

    def setup(self):
        print("--- Image Generator Setup ---")
        self.load_positions()
        self.load_templates()
        self.check_fonts()
        print("--- Image Generator Setup Complete ---")

    def check_fonts(self):
        """폰트 디렉토리와 파일들을 확인"""
        print(f"→ 폰트 디렉토리: {self.fonts_dir}")
        
        if not self.fonts_dir.exists():
            print(f"❌ 폰트 디렉토리 없음")
            return
        
        font_files = list(self.fonts_dir.glob("*.ttf")) + list(self.fonts_dir.glob("*.otf"))
        print(f"→ 폰트 파일: {len(font_files)}개")
        
        # 주요 폰트들만 테스트
        test_fonts = [
            ("Inter_18pt-Regular", "영어"),
            ("NanumSquareNeo-bRg", "한국어")
        ]
        
        for font_name, desc in test_fonts:
            try:
                self.get_font(font_name, 20)
                print(f"✅ {desc} 폰트 준비")
            except Exception:
                print(f"❌ {desc} 폰트 실패")

    def load_default_font(self):
        """기본 폰트 로드 테스트 (deprecated - check_fonts로 대체)"""
        pass

    def _hex_to_rgba(self, hex_color):
        """HEX 색상을 RGBA 튜플로 변환"""
        if not hex_color or not isinstance(hex_color, str):
            return (0, 0, 0, 255)
            
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) + (255,)
        elif len(hex_color) == 8:
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4, 6))
        return (0, 0, 0, 255)

    def _select_template_by_weather(self, weather_summary, language='en', format='post'):
        """날씨에 따른 템플릿 선택"""
        combined_weather = weather_summary.get('combined', 'SUNNY').upper()
        temp_max = weather_summary.get('temp_max')
        print(f" → 날씨 상태: {combined_weather}, 최고기온: {temp_max}°C")

        # 템플릿 타입 결정
        template_type = 'sunny'  # 기본값
        if 'HEATWAVE' in combined_weather: 
            template_type = 'heatwave'
        elif 'HEAVY_RAIN' in combined_weather: 
            template_type = 'heavyrain'
        elif 'TYPHOON' in combined_weather: 
            template_type = 'typhoon'
        elif 'SHOWER' in combined_weather: 
            template_type = 'shower'
        elif 'RAINY' in combined_weather: 
            template_type = 'rainy'
        elif 'SNOW' in combined_weather: 
            template_type = 'snowy'
        elif temp_max is not None and temp_max >= 30: 
            template_type = 'hot'
        elif 'CLOUDY' in combined_weather or 'PARTLY_CLOUDY' in combined_weather: 
            template_type = 'cloudy'

        # 언어별 템플릿 파일명 생성
        lang_suffix = '_ko' if language == 'ko' else ''
        template_filename = f"{format}_{template_type}{lang_suffix}.png"
        
        # 1. 언어별 템플릿 시도
        template_path = self._get_template_path(template_filename, format)
        if template_path.exists():
            print(f" → 선택된 템플릿: {template_filename}")
            return template_filename

        # 2. 언어별 템플릿이 없으면 기본(영어) 템플릿으로 대체
        if lang_suffix:
            template_filename = f"{format}_{template_type}.png"
            template_path = self._get_template_path(template_filename, format)
            if template_path.exists():
                print(f" → (대체) 선택된 템플릿: {template_filename}")
                return template_filename
            
        print(f" → 최종 선택된 템플릿: {template_filename}")
        return template_filename

    def _get_template_path(self, template_filename, format='post'):
        """템플릿 파일 경로 반환"""
        if format == 'post':
            return self.templates_dir / "posts" / template_filename
        else:
            return self.templates_dir / template_filename

    def _draw_text(self, image, text, config, language='en', **kwargs):
        """텍스트를 이미지에 그리는 통합 함수"""
        if not text or text == "N/A" or str(text).strip() == "": 
            return
        if not config.get("visible", True): 
            return
            
        font_size = config.get("font_size", 30)
        if font_size == 0: 
            return

        # 폰트 결정
        font_name = kwargs.get("font_name_override")
        if not font_name:
            if language == 'ko' and 'font_name_ko' in config:
                font_name = config['font_name_ko']
            else:
                font_name = config.get("font_name", "Inter_18pt-Regular")

        font = self.get_font(font_name, font_size)
        
        # 색상, 위치, 정렬 설정
        color = self._hex_to_rgba(kwargs.get("color", config.get("color", "#000000")))
        align = kwargs.get("align", config.get("align", "left"))
        x = kwargs.get("x", config.get("x", 0))
        y = kwargs.get("y", config.get("y", 0))
        max_width = config.get("max_width")

        draw = ImageDraw.Draw(image)
        
        # 텍스트 래핑 처리
        text_to_draw = text
        if max_width:
            lines = []
            words = str(text).split(' ')
            current_line = []
            for word in words:
                test_line = ' '.join(current_line + [word])
                if draw.textlength(test_line, font=font) <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(' '.join(current_line))
            text_to_draw = "\n".join(lines)

        # 정렬 처리
        if align == "center":
            bbox = draw.textbbox((0, 0), text_to_draw, font=font)
            text_width = bbox[2] - bbox[0]
            x = x - text_width // 2
        elif align == "right":
            bbox = draw.textbbox((0, 0), text_to_draw, font=font)
            text_width = bbox[2] - bbox[0]
            x = x - text_width

        # 텍스트 그리기
        try:
            with Pilmoji(image) as pilmoji:
                pilmoji.text((x, y), text_to_draw, fill=color, font=font)
        except Exception:
            # Pilmoji 실패 시 일반 텍스트로 대체
            try:
                draw.text((x, y), text_to_draw, fill=color, font=font)
            except Exception:
                # 최후의 수단: 기본 폰트
                default_font = ImageFont.load_default()
                draw.text((x, y), text_to_draw, fill=color, font=default_font)

    def _format_time_hhmm_to_readable(self, time_str):
        """HHMM 형식을 HH:MM으로 변환"""
        if not time_str or time_str == "N/A" or len(str(time_str)) != 4: 
            return "N/A"
        try: 
            time_str = str(time_str)
            return f"{time_str[:2]}:{time_str[2:]}"
        except: 
            return "N/A"
    
    def _format_duration_to_hm(self, duration_str, language='en'):
        """지속시간을 언어별로 포맷"""
        if not duration_str or duration_str == "N/A": 
            return "N/A"
        
        duration_str = str(duration_str)
        if language == 'ko':
            return duration_str.replace("h", "시간").replace("m", "분")
        return duration_str.replace("h", "H").replace("m", "M")
    
    def _get_uv_level_info(self, uv_index, language='en'):
        """UV 지수에 따른 레벨 정보 반환"""
        try: 
            uv_val = int(uv_index) if uv_index != "N/A" else 0
        except: 
            return ("알 수 없음", "⚪") if language == 'ko' else ("UNKNOWN", "⚪")
        
        levels_ko = {0: "낮음", 3: "보통", 6: "높음", 8: "매우 높음", 11: "위험"}
        levels_en = {0: "LOW", 3: "MODERATE", 6: "HIGH", 8: "VERY HIGH", 11: "EXTREME"}
        emojis = {0: "🟢", 3: "🟡", 6: "🟠", 8: "🔴", 11: "🟣"}
        
        levels = levels_ko if language == 'ko' else levels_en
        
        level_text = levels[0]
        emoji = emojis[0]
        for threshold, text in sorted(levels.items(), reverse=True):
            if uv_val >= threshold:
                level_text = text
                break
        for threshold, e in sorted(emojis.items(), reverse=True):
            if uv_val >= threshold:
                emoji = e
                break
        return level_text, emoji

    def _prepare_warning_text(self, warnings, language='en'):
        """특보 텍스트 준비 (언어별)"""
        if not warnings or not isinstance(warnings, dict):
            return None
            
        warn_type = warnings.get('type')
        warn_level = warnings.get('level')
        
        if not warn_type or not warn_level:
            return None
            
        if language == 'ko':
            return f"{warn_type} {warn_level}"
        else:
            # 영어 변환
            level_en = 'Advisory' if warn_level == '주의보' else 'Warning'
            type_en_map = {'폭염': 'Heatwave', '호우': 'Heavy Rain', '태풍': 'Typhoon'}
            type_en = type_en_map.get(warn_type, 'Weather')
            return f"{type_en} {level_en}"

    def create_post_image(self, data, phrase, activity_index_am, activity_index_pm, language='en'):
        """포스트 이미지 생성"""
        print(f"포스트 이미지 생성 시작 ({language.upper()})...")
        
        # 템플릿 선택 및 로드
        template_filename = self._select_template_by_weather(data['weather_summary'], language, 'post')
        template_path = self._get_template_path(template_filename, 'post')
        
        if template_path.exists():
            img = Image.open(template_path).convert("RGBA")
            print(f" → 템플릿 로드 성공: {template_path}")
        else:
            # 기본 이미지 생성
            size = tuple(self.positions.get("post_template", {}).get("size", [1080, 1350]))
            bg_color = self._hex_to_rgba(self.positions.get("post_template", {}).get("background_color", "#FFFFFF"))
            img = Image.new("RGBA", size, bg_color)
            print(f" ⚠️ 템플릿 없음, 기본 배경 생성: {template_path}")
        
        # positions 설정 가져오기
        pos = self.positions.get("post_template", {}).get("elements", {})
        if not pos:
            print("❌ positions 설정을 찾을 수 없습니다!")
            return None, {}
        
        # 데이터 추출
        ws = data['weather_summary']
        indices = data['indices']
        astro = data['astro_info']
        target_date = data['info']['target_date']
        warnings = data.get('warnings')
        
        try:
            date_obj = datetime.datetime.strptime(target_date, "%Y%m%d")
        except:
            date_obj = datetime.datetime.now()

        # ========================================
        # 언어별 텍스트 변수 생성
        # ========================================
        
        # 날짜 텍스트
        if language == 'ko':
            weekdays = ["월", "화", "수", "목", "금", "토", "일"]
            date_text = f"{date_obj.month}월 {date_obj.day}일 {weekdays[date_obj.weekday()]}요일"
        else:
            date_text = date_obj.strftime('%B %d, %A')

        # 온도 텍스트
        temp_max = ws.get('temp_max')
        temp_min = ws.get('temp_min')
        temp_max_text = f"{int(temp_max)}°" if temp_max is not None else "N/A"
        temp_min_text = f"{int(temp_min)}°" if temp_min is not None else "N/A"

        # 어제와 온도 비교
        temp_diff = ws.get('temp_diff')
        temp_diff_text = ""
        if temp_diff is not None:
            if language == 'ko':
                if temp_diff > 0: 
                    temp_diff_text = f"어제보다 {temp_diff:.1f}° 높아요"
                elif temp_diff < 0: 
                    temp_diff_text = f"어제보다 {abs(temp_diff):.1f}° 낮아요"
                else: 
                    temp_diff_text = "어제와 비슷해요"
            else:
                if temp_diff > 0: 
                    temp_diff_text = f"{temp_diff:.1f}° higher than yesterday"
                elif temp_diff < 0: 
                    temp_diff_text = f"{abs(temp_diff):.1f}° lower than yesterday"
                else: 
                    temp_diff_text = "Same as yesterday"
        else:
            temp_diff_text = "비교 데이터 없음" if language == 'ko' else "No comparison data"

        # 기타 데이터
        humidity_text = f"{ws.get('avg_humidity', 0)}%"
        wind_text = f"{ws.get('max_wind_speed', 0)} m/s"
        rain_probability_text = f"{ws.get('rain_prob_max', 0)}%"

        # 자외선 정보
        uv_index_value = indices.get('uv_index', 'N/A')
        uv_level, _ = self._get_uv_level_info(uv_index_value, language)
        uv_number_text = str(uv_index_value)
        uv_level_text = uv_level

        # 대기질 정보 (언어별 처리)
        air_pm10 = indices.get('air_quality_pm10', {})
        air_pm25 = indices.get('air_quality_pm25', {})
        
        def translate_air_status(status, language):
            if language == 'ko':
                translations = {
                    'Good': '좋음', 'Moderate': '보통', 
                    'Bad': '나쁨', 'Very Bad': '매우 나쁨'
                }
                return translations.get(status, status)
            return status
        
        pm10_status = translate_air_status(air_pm10.get('status', 'N/A'), language)
        pm25_status = translate_air_status(air_pm25.get('status', 'N/A'), language)
        
        air_pm10_text = f"PM10: {pm10_status} {air_pm10.get('emoji', '⚪')}"
        air_pm25_text = f"PM2.5: {pm25_status} {air_pm25.get('emoji', '⚪')}"

        # 강수 정보 (이미 언어별로 처리됨)
        rain_details = ws.get('detailed_rain_times', [])
        if isinstance(rain_details, list) and rain_details:
            rain_text = "\n".join(rain_details)
        else:
            # 강수 확률로 대체
            rain_prob_max = ws.get('rain_prob_max', 0)
            if language == 'ko':
                if rain_prob_max > 70:
                    rain_text = "비 올 가능성 높음"
                elif rain_prob_max > 30:
                    rain_text = "비 올 수도"
                else:
                    rain_text = "비 안 올 것 같음"
            else:
                if rain_prob_max > 70:
                    rain_text = "Rain likely"
                elif rain_prob_max > 30:
                    rain_text = "Possible rain"
                else:
                    rain_text = "No rain expected"

        # 천체 정보
        sunrise_text = self._format_time_hhmm_to_readable(astro.get('sunrise', 'N/A'))
        sunset_text = self._format_time_hhmm_to_readable(astro.get('sunset', 'N/A'))
        daylight_text = self._format_duration_to_hm(astro.get('daylight_duration', 'N/A'), language)
        night_text = self._format_duration_to_hm(astro.get('night_duration', 'N/A'), language)
        moonrise_text = self._format_time_hhmm_to_readable(astro.get('moonrise', 'N/A'))
        moonset_text = self._format_time_hhmm_to_readable(astro.get('moonset', 'N/A'))
        moon_emoji_text = astro.get('moon_emoji', '🌑')
        
        if language == 'ko':
            moon_phase_name = astro.get('moon_phase_ko', 'N/A')
        else:
            moon_phase_name = astro.get('moon_phase_simple', 'N/A')

        # 야외활동 지수 포맷
        def format_index_text(index_data):
            grade = index_data.get('grade', 'N/A')
            reason = index_data.get('reason')
            text = f"{grade}"
            if grade in ["Excellent", "Good", "최상", "좋음"]: 
                text += " (*)"
            if reason: 
                text += f" ({reason})"
            return text

        activity_am_text = format_index_text(activity_index_am)
        activity_pm_text = format_index_text(activity_index_pm)

        # ========================================
        # 특보 확인 및 텍스트 그리기
        # ========================================
        
        # 특보 여부 확인
        is_major_warning = False
        warning_text = None
        if warnings and isinstance(warnings, dict):
            warn_type = warnings.get('type')
            if warn_type in ['폭염', '호우', '태풍']:
                is_major_warning = True
                warning_text = self._prepare_warning_text(warnings, language)

        # 특보가 있을 경우 특별 처리
        if is_major_warning and warning_text:
            print(f" → 특보 발효: {warning_text}")
            
            # 특보용 날짜 위치 사용
            date_config = pos.get("date_for_warning", pos.get("date", {}))
            if date_config:
                self._draw_text(img, date_text, date_config, language)
            
            # 특보 정보 위치 사용
            warning_config = pos.get("warning_info", pos.get("catch_phrase", {}))
            if warning_config:
                self._draw_text(img, warning_text, warning_config, language)
        else:
            # 일반 날씨: 기본 위치 사용
            date_config = pos.get("date", {})
            if date_config:
                self._draw_text(img, date_text, date_config, language)
            
            catch_phrase_config = pos.get("catch_phrase", {})
            if catch_phrase_config:
                self._draw_text(img, phrase, catch_phrase_config, language)

        # ========================================
        # 나머지 모든 텍스트 그리기 (language 파라미터 추가)
        # ========================================
        
        text_elements = [
            ("temp_max", temp_max_text),
            ("temp_min", temp_min_text),
            ("temp_diff", temp_diff_text),
            ("rain_info", rain_text),
            ("rain_probability", rain_probability_text),
            ("humidity", humidity_text),
            ("wind", wind_text),
            ("uv_number", uv_number_text),
            ("uv_level", uv_level_text),
            ("air_quality_pm10", air_pm10_text),
            ("air_quality_pm25", air_pm25_text),
            ("daylight", daylight_text),
            ("night", night_text),
            ("sunrise", sunrise_text),
            ("sunset", sunset_text),
            ("moonrise", moonrise_text),
            ("moonset", moonset_text),
            ("moon_emoji", moon_emoji_text),
            ("moon_phase", moon_phase_name),
            ("activity_index_am", activity_am_text),
            ("activity_index_pm", activity_pm_text),
        ]

        for element_key, text_value in text_elements:
            if element_key in pos and text_value:
                try:
                    self._draw_text(img, text_value, pos[element_key], language)
                except Exception as e:
                    print(f"⚠️ {element_key} 텍스트 그리기 실패: {e}")

        # ========================================
        # 이미지 저장
        # ========================================
        
        # 출력 디렉토리 생성
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"weather_post_{language}_{timestamp}.png"
        
        try:
            img.save(output_path, "PNG")
            print(f"✅ 포스트 이미지 생성 완료: {output_path}")
            return output_path, {}
        except Exception as e:
            print(f"❌ 이미지 저장 실패: {e}")
            return None, {}

    def get_font(self, font_name="Inter_18pt-Regular", size=20):
        """폰트를 로드하는 함수 (한국어/영어 동일한 방식 처리)"""
        
        # 1. 프로젝트 폰트 디렉토리에서 찾기 (정확한 이름으로)
        if font_name in self.font_paths:
            font_path = self.font_paths[font_name]
            if font_path.exists():
                try:
                    font = ImageFont.truetype(str(font_path), size, encoding='unic')
                    return font
                except (IOError, OSError) as e:
                    print(f"⚠️ 폰트 로드 실패: {font_name}")
        
        # 2. 확장자 있는 파일명으로 시도
        for ext in ['.ttf', '.otf', '.ttc']:
            font_path = self.fonts_dir / f"{font_name}{ext}"
            if font_path.exists():
                try:
                    return ImageFont.truetype(str(font_path), size, encoding='unic')
                except (IOError, OSError):
                    continue
        
        # 3. 한국어 폰트 요청 시 대체 시도
        if 'Nanum' in font_name or font_name in ['NanumSquareNeo-bRg', 'NanumSquareNeo-cBd', 'NanumSquareNeo-dEb', 'NanumSquareNeo-eHv']:
            fallback_fonts = ["malgun.ttf", "NanumGothic.ttf", "gulim.ttc"]
            for fallback in fallback_fonts:
                try:
                    return ImageFont.truetype(fallback, size, encoding='unic')
                except (IOError, OSError):
                    continue
            print(f"⚠️ 한국어 폰트 실패, 영어 폰트로 대체: {font_name}")
            return self.get_font("Inter_18pt-Regular", size)
        
        # 4. 영어 폰트 대체
        system_fonts = ["arial.ttf", "calibri.ttf", "tahoma.ttf"]
        for sys_font in system_fonts:
            try:
                return ImageFont.truetype(sys_font, size, encoding='unic')
            except (IOError, OSError):
                continue
        
        # 5. 최후의 수단
        print(f"❌ 모든 폰트 실패, 기본 폰트 사용: {font_name}")
        try:
            return ImageFont.load_default(size)
        except:
            return ImageFont.load_default()

    def create_story_image(self, data, phrase, language='en'):
        """스토리 이미지 생성 (향후 구현)"""
        print(f"스토리 이미지 생성은 현재 구현되지 않았습니다 ({language}).")
        return None, None
        
    def test_coordinates(self):
        """좌표 테스트 (향후 구현)"""
        pass