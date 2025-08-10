# coordinate_test_fixed.py
# 좌표 변경이 제대로 적용되도록 수정된 테스트 스크립트

from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji
from pathlib import Path
import json

def test_coordinates():
    # 기본 경로 설정 (스크립트 위치 기반 동적 경로)
    # main.py나 image_generator.py와 동일한 방식으로, 테스트 파일의 위치를 기준으로 경로를 설정합니다.
    script_root = Path(__file__).parent # 이 파일(coordinate_test.py)이 있는 프로젝트 루트
    base_dir = script_root / "weather_service"
    templates_dir = base_dir / "templates" / "posts"
    fonts_dir = base_dir / "fonts"
    config_dir = base_dir / "config"
    output_dir = base_dir / "output"

    print("=== 🛠️ 좌표 테스트 시작 ===")
    print(f"📁 Base Dir: {base_dir}")
    print(f"📁 Templates Dir: {templates_dir}")
    print(f"📁 Fonts Dir: {fonts_dir}")

    # positions.json 로드 및 디버깅
    positions = {}
    config_file = config_dir / "positions.json"
    
    try:
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                positions = json.load(f)
            print(f"✅ positions.json 로드 성공: {len(positions)} 템플릿 발견")
            print(f"📋 템플릿 목록: {list(positions.keys())}")
        else:
            print(f"❌ positions.json 파일 없음: {config_file}")
            return
    except Exception as e:
        print(f"❌ positions.json 로드 실패: {e}")
        return

    # 폰트 로드 헬퍼 함수 (디버깅 강화)
    def load_font(font_name, size):
        print(f"🔍 폰트 찾는 중: {font_name} ({size}px)")
        
        if not font_name:
            print("⚠️ 폰트 이름이 없음, 기본 폰트 사용")
            return ImageFont.load_default()
        
        for ext in ['.ttf', '.otf', '.woff']:
            font_path = fonts_dir / f"{font_name}{ext}"
            if font_path.exists():
                try:
                    font = ImageFont.truetype(str(font_path), size)
                    print(f"✅ 폰트 로드 성공: {font_path}")
                    return font
                except Exception as e:
                    print(f"❌ 폰트 로드 실패: {font_path} - {e}")
                    continue
        
        print(f"❌ 폰트 못 찾음: {font_name}, 기본 폰트 사용")
        return ImageFont.load_default()

    # 배경 이미지 로드 (여러 파일명 시도)
    background_files = ["post_sunny.png", "sunny.png", "post_template.png"]
    img = None
    
    for bg_file in background_files:
        bg_path = templates_dir / bg_file
        if bg_path.exists():
            try:
                img = Image.open(bg_path).convert("RGBA")
                print(f"✅ 배경 로드 성공: {bg_path}")
                break
            except Exception as e:
                print(f"❌ 배경 로드 실패: {bg_path} - {e}")
    
    if img is None:
        print("⚠️ 배경 이미지 없음, 기본 배경 생성")
        img = Image.new("RGBA", (1080, 1350), (255, 255, 255, 255))
    
    draw = ImageDraw.Draw(img)
    
    # 템플릿 설정 가져오기
    template_config = positions.get("post_template", {})
    elements_config = template_config.get("elements", {})
    
    if not elements_config:
        print("❌ post_template의 elements 설정이 없습니다!")
        return
    
    print(f"📋 요소 개수: {len(elements_config)}")
    print(f"📋 요소 목록: {list(elements_config.keys())}")

    # 더미 데이터 (테스트용)
    dummy_data = {
        "date": "JULY 23, WEDNESDAY",
        "catch_phrase": "TODAY'S WEATHER IS AMAZING!",
        "temp_max": "32°",
        "temp_min": "25°", 
        "temp_diff": "2.0°C HIGHER THAN YESTERDAY",
        "rain_info": "💧 HIGH CHANCE OF RAIN: 09:00-12:00",
        "rain_probability": "40%",
        "humidity": "70.0%",
        "wind": "2.1 m/s", 
        "uv_number": "8",
        "uv_level": "VERY HIGH",
        "uv_emoji": "🔴",
        "air_quality_status": "GOOD",
        "air_quality_emoji": "🟢",
        "daylight": "14H 19M",
        "night": "09H 41M", 
        "sunrise": "05:29",
        "sunset": "19:48",
        "moonrise": "03:07",
        "moonset": "18:58",
        "moon_emoji": "🌘",
        "moon_phase": "WANING CRESCENT"
    }

    successful_draws = 0
    failed_draws = 0

    for element_name, text_content in dummy_data.items():
        print(f"\n🎯 처리 중: {element_name}")
        
        config = elements_config.get(element_name)
        if not config:
            print(f"⚠️ {element_name} 설정 없음, 건너뜀")
            failed_draws += 1
            continue

        # 설정값 추출
        x = config.get("x")
        y = config.get("y") 
        font_name = config.get("font_name", "Inter_18pt-Regular")
        font_size = config.get("font_size", 20)
        color = config.get("color", "#000000")
        align = config.get("align", "left")
        max_width = config.get("max_width")
        
        print(f"  📍 좌표: ({x}, {y})")
        print(f"  🔤 폰트: {font_name} {font_size}px")
        print(f"  🎨 색상: {color}")
        print(f"  📐 정렬: {align}")

        if x is None or y is None:
            print(f"❌ {element_name} 좌표 없음")
            failed_draws += 1
            continue

        # 폰트 로드
        font = load_font(font_name, font_size)
        
        # 색상 처리 (hex를 RGB로 변환)
        try:
            if isinstance(color, str) and color.startswith('#'):
                hex_color = color.lstrip('#')
                if len(hex_color) == 6:
                    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                elif len(hex_color) == 8:
                    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4, 6))
                else:
                    rgb_color = (0, 0, 0)
            else:
                rgb_color = color if isinstance(color, tuple) else (0, 0, 0)
        except:
            rgb_color = (0, 0, 0)
            print(f"⚠️ 색상 변환 실패, 검은색 사용: {color}")

        # 텍스트 준비
        text_to_draw = str(text_content)
        
        # 여러 줄 텍스트 처리 (max_width 있을 때)
        if max_width and max_width > 0:
            try:
                lines = []
                words = text_to_draw.split(' ')
                current_line = []
                for word in words:
                    test_line = ' '.join(current_line + [word])
                    # PIL 버전 호환성을 위해 여러 방법 시도
                    try:
                        text_width = draw.textlength(test_line, font=font)
                    except AttributeError:
                        try:
                            text_width = font.getsize(test_line)[0]
                        except AttributeError:
                            text_width = len(test_line) * font_size * 0.6  # 대략적 계산
                    
                    if text_width <= max_width:
                        current_line.append(word)
                    else:
                        if current_line:
                            lines.append(' '.join(current_line))
                        current_line = [word]
                lines.append(' '.join(current_line))
                text_to_draw = "\n".join(lines)
                print(f"  📄 텍스트 줄바꿈: {len(lines)}줄")
            except Exception as e:
                print(f"⚠️ 텍스트 줄바꿈 실패: {e}")

        # 중앙 정렬 처리
        draw_x = x
        if align == "center":
            try:
                bbox = draw.textbbox((0, 0), text_to_draw, font=font)
                text_width = bbox[2] - bbox[0]
                draw_x = x - text_width // 2
                print(f"  📐 중앙정렬: {x} → {draw_x}")
            except Exception as e:
                print(f"⚠️ 중앙정렬 계산 실패: {e}")

        # 텍스트 그리기
        try:
            # 이모지 포함 여부 확인
            has_emoji = any(ord(char) > 127 for char in text_to_draw)
            
            if has_emoji:
                print(f"  🎭 이모지 포함, Pilmoji 사용")
                with Pilmoji(img) as pilmoji:
                    pilmoji.text((draw_x, y), text_to_draw, fill=rgb_color, font=font)
            else:
                print(f"  ✏️ 일반 텍스트, PIL 사용")
                draw.text((draw_x, y), text_to_draw, fill=rgb_color, font=font)
            
            # 기준점 표시 (빨간 점)
            draw.ellipse([(x-5, y-5), (x+5, y+5)], fill='red')
            
            print(f"  ✅ 그리기 성공!")
            successful_draws += 1
            
        except Exception as e:
            print(f"  ❌ 그리기 실패: {e}")
            failed_draws += 1

    # 결과 저장
    try:
        save_path = output_dir / "coordinate_test_debug.png"
        img.save(save_path)
        print(f"\n✅ 저장 성공: {save_path}")
    except Exception as e:
        print(f"\n❌ 저장 실패: {e}")

    # 최종 결과
    print(f"\n=== 📊 테스트 결과 ===")
    print(f"✅ 성공: {successful_draws}개")
    print(f"❌ 실패: {failed_draws}개")
    print(f"📁 출력 파일: coordinate_test_debug.png")
    
    if failed_draws > 0:
        print(f"\n💡 실패 원인 체크리스트:")
        print(f"   1. positions.json에 해당 요소 설정이 있는가?")
        print(f"   2. 폰트 파일이 fonts/ 폴더에 있는가?")
        print(f"   3. 좌표값(x, y)이 올바른가?")
        print(f"   4. 색상 형식이 올바른가? (#RRGGBB 또는 #RRGGBBAA)")

if __name__ == "__main__":
    test_coordinates()