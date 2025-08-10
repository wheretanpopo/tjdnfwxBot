import random
from datetime import datetime

class WeatherPhraseGenerator:
    def __init__(self):
        # 1순위: 놓치기 아쉬운 특별한 날
        self.special_moon_phrases = [
            "보름달 떠. 잘 보일 거야",
            "오늘 밤 보름달이야.",
            "보름달 뜬다. 밖에서 봐",
            "달 진짜 예쁠 것 같아. 보름달이야",
            "오늘 밤 달구경하기 좋겠어",
            "보름달 뜨는 날엔 늑대가 된다던데",
        ]
        
        self.perfect_weather_phrases = [
            "날씨 완벽해. 밖에 나가기 딱 좋아",
            "날씨 최고야. 어디든 가고 싶어",
            "완벽한 날씨네. 야외활동하기 좋아",
            "오늘 야외 운동 어때?",
            "오늘 같은 날에 러닝하기 좋아",
            "이런 날 집에만 있으면 아까워",
            "날씨가 이렇게 좋으면 불법이지",
        ]
        
        # 2순위: 건강 및 안전 직결 상황
        self.temp_drop_phrases = [
            "갑자기 쌀쌀해졌네. 옷 더 챙겨 입자",
            "기온 뚝 떨어졌어. 몸 조심해", 
            "전날보다 완전 추워졌대. 준비 안 했지?",
            "어제가 거짓말 같아. 갑자기 추워",
            "기온 급락할거래. 옷차림 조절 잘해"
        ]
        
        self.temp_rise_phrases = [
            "갑자기 더워졌네. 얇게 입어",
            "기온 확 올랐어. 낮엔 한여름이야",
            "전날보다 완전 더워졌어. 놀랐지?", 
            "지구온난화가 하루 만에 온 것 같아",
            "온도 급상승했네. 놀라지 마"
        ]
        
        self.extreme_cold_wind_phrases = [
            "춥고 바람까지. 완전 얼어붙을 것 같아",
            "영하인데 바람까지 불어. 진짜 춥겠어",
            "추위에 바람까지. 외출 조심해",
            "춥고 바람 세서 체감온도 더 낮아",
            "밖이랑 냉장고 안이랑 차이가 없음",
        ]
        
        # **불쾌지수 관련 문구 추가** (누락되어 있었음)
        self.extreme_hot_humid_phrases = [
            "더운데 습하기까지 해. 찜통이야",
            "덥고 끈적해. 불쾌지수 최고야", 
            "더위에 습기까지. 에어컨 필수야",
            "찜통 더위야. 밖에 나가지 마",
            "사우나 밖에 또 다른 사우나가 있네",
            "더위에 습도까지. 완전 사우나야",
            "끈적끈적해. 불쾌지수 폭발",
            "찜통에서 사는 기분이야"
        ]
        
        self.rain_wind_phrases = [
            "비바람 싫어. 우산 뒤집어질 듯",
            "비바람이야. 외출하지 마",
            "비에 바람까지. 조심해서 다녀",
            "날씨 구려서 집에서 넷플릭스나 보려고"
        ]
        
        self.extreme_hot_phrases = [
            "아스팔트에서 계란 후라이 가능",
            "찜통 더위. 에어컨으로도 안 돼"
        ]
        
        self.extreme_cold_phrases = [
            "완전 춥네. 핫팩 온몸에 붙여야겠어",
            "한파래. 꽁꽁 싸매고 다녀",
            "추워서 이불 속에서 동면하고 싶어"
        ]
        
        self.dust_phrases = [
            "미세먼지 심해. 마스크 써",
            "공기 안 좋아. 밖에 나가지 마",
            "미세먼지 농도 높네. 창문 닫아",
            "미세먼지 최악이야. 마스크 필수",
            "미세먼지 때문인지 시야가 뿌옇더라."
        ]
        
        self.high_uv_phrases = [
            "자외선 진짜 강해. 선크림 발라",
            "UV 지수 높아. 양산 쓰고 다녀",
            "햇빛 독해. 모자 써",
            "자외선 차단 필수야. 피부 탈 거야",
            "햇빛 강렬해. 그늘로 다녀",
            "UV 폭탄이야. 선크림 필수",
            "자외선 강해서 5분만 있어도 탈 것 같아"
        ]
        
        self.heavy_rain_phrases = [
            "비 진짜 많이 올 거야. 준비해",
            "장대비 예보야. 외출 조심해",
            "비 엄청 쏟아질 것 같아",
            "물폭탄 온다고 해. 조심해",
            "하늘에서 수도꼭지 틀어놨나 봐",
        ]
        
        self.rain_high_prob_phrases = [
            "비 많이 올 확률 높아. 우산 챙겨",
            "비 올 가능성 커. 준비해",
            "비 확률 높네. 우산 꼭 가져가",
            "비 올 것 같아. 대비해",
            "거의 비 올 것 같아"
        ]
        
        self.tropical_night_phrases = [
            "열대야야. 밤에도 더울 거야",
            "한여름도 아닌데 밤에도 더워"
        ]
        
        self.strong_wind_phrases = [
            "바람 진짜 세게 불어. 조심해",
            "오늘 바람 심해. 모자 날아갈 듯",
            "강풍 분다고 해. 외출 조심해",
            "바람 완전 세네. 날라갈 뻔",
            "강한 바람 불 예정이야. 주의해",
            "바람 때문에 머리 난리 나겠다",
            "돌풍 주의. 간판도 조심해"
        ]
        
        self.large_temp_diff_phrases = [
            "일교차 심해. 아침엔 춥다가 낮엔 더워",
            "기온차 커. 겉옷 하나 챙겨",
            "아침 저녁 춥고 낮엔 더울 거야",
            "일교차 크니까 감기 조심해",
            "아침에 쌀쌀한데 오후엔 더워진다네",
            "기온이 롤러코스터 타는 날이네",
            "일교차 심하네. 옷차림 고민이 돼"
        ]
        
        # 3순위: 일상적인 날씨 정보
        self.sunny_phrases = [
            "오늘 날씨 맑아. 진짜 좋네",
            "해 진짜 좋다. 기분 좋을 것 같아",
            "맑고 쾌청해. 빨래 널기 좋겠어",
            "오늘 햇살 진짜 좋을 것 같아",
            "완전 화창해. 산책하기 좋아",
            "하늘 맑아. 기분도 좋아질 듯",
            "비타민 D 충전하는 날이야"
        ]
        
        self.cloudy_phrases = [
            "흐린 날이야.",
            "구름이 하늘 다 덮었네",
            "오늘 하늘 회색빛이야",
            "흐리지만 비는 안 올 것 같아",
            "하늘이 우울한 것 같아. 나랑 똑같네",
        ]
        
        self.partly_cloudy_phrases = [
            "구름 조금 끼었어. 적당해",
            "하늘 반반이야. 괜찮은 날씨",
            "구름 있긴 한데 나쁘지 않아",
            "반쯤 흐린 날씨야. 적당해",
        ]
        
        self.hot_phrases = [
            "좀 더워. 얇게 입고 다녀",
            "더위 좀 있을 거야. 준비해", 
            "더워지고 있어. 시원하게 입어",
            "더위 느껴질 거야. 가볍게 입어",
            "따뜻하다 못해 좀 더워",
            "이제 에어컨 켜도 유난 아니지?"
        ]
        
        self.cold_phrases = [
            "좀 쌀쌀해. 얇은 겉옷 입어",
            "선선해. 가볍게 걸쳐",
            "조금 쌀쌀할 것 같아. 준비해",
            "얇은 카디건 하나 걸쳐",
            "쌀쌀해지네. 감기 조심해",
            "좀 서늘할 것 같아. 옷 챙겨",
            "조금 차가워. 따뜻하게 입어",
            "쌀쌀한 날씨야. 건강 챙겨",
            "서늘해지고 있어. 감기 조심해",
            "좀 차갑네. 몸 따뜻하게 해",
            "가을이 살금살금 왔나 봐"
        ]
        
        self.normal_temp_phrases = [
            "날씨 적당해. 나가기 좋을 것 같아",
            "온도 완전 적당해. 편해",
            "기온 괜찮네. 옷차림 고민 없겠어",
            "날씨 포근해. 기분 좋아",
            "온도 딱 맞아. 쾌적할 것 같아",
            "기온 적절해. 뭐든 하기 좋겠어",
            "날씨 평온해. 편안한 하루 될 듯",
            "기온 적당해. 활동하기 좋아",
            "인간에게 최적화된 온도 설정 완료"
        ]
        
        self.light_rain_phrases = [
            "비 올 수도 있어. 우산 챙겨",
            "비 올까 말까 해",
            "비 조금 올 수도 있어",
            "우산 들고 다니는 게 좋겠어",
            "혹시 모르니까 우산 챙겨",
            "비 살짝 올 수도 있어",
            "비 올 확률 30%. 우산 들고 나갈지 고민 중"
        ]
        
        self.rainy_phrases = [
            "비 와. 우산 꼭 챙겨",
            "비 온다고 해. 준비해",
            "오늘 비 온대. 우산 가져가",
            "비 내려. 외출 조심해",
            "비 예보야. 우산 필수",
            "오늘 비 올 거야. 대비해",
            "비 온다네. 젖지 않게 조심해",
            "비 내릴 예정이야. 우산 챙겨",
            "하늘이 울고 있어. 우산 가져가"
        ]
        
        self.snow_phrases = [
            "눈 온대. 미끄러지지 마",
            "눈 내린다고 해. 조심해서 다녀",
            "오늘 눈 올 거야. 외출 조심해",
            "눈 예보야. 길 조심해",
            "눈 온다네. 미끄러울 것 같아",
            "눈 내릴 예정이야. 넘어지지 마",
            "오늘 눈 온대. 따뜻하게 입어",
            "눈 와. 차 운전 조심해",
            "하늘에서 솜사탕 뿌린다"
        ]
        
        self.shower_phrases = [
            "소나기 온다고 해",
            "소나기 예보야. 우산 챙겨",
            "갑자기 비 올 수 있어",
            "소나기 올 수 있어",
            "소나기성 비 온대",
            "갑작스럽게 비 올 수도 있어",
            "소나기 확률 높아",
            "순간 비 올 것 같아",
            "하늘이 갑자기 울 예정. 나처럼"
        ]

    def generate_phrase(self, final_data):
        weather = final_data.get('weather_summary', {})
        indices = final_data.get('indices', {})
        astro = final_data.get('astro_info', {})
        warnings = final_data.get('warnings')
        info = final_data.get('info', {})
        date_obj = info.get('date_object')

        # 특보별 캐치프레이즈 (템플릿이 없는 특보용)
        self.warning_phrases = {
            "한파": [
                "한파 특보야. 꽁꽁 얼겠어",
                "한파 경보 발효. 완전 추워질 거야",
                "한파 주의보래. 핫팩 준비해",
                "혹한기야. 동상 조심해"
            ],
            "대설": [
                "대설 특보야. 눈 많이 와",
                "대설 경보래. 외출 조심해",
                "눈폭탄 온다고 해",
                "대설 주의보야. 길 조심해"
            ],
            "강풍": [
                "강풍 특보야. 바람 진짜 세겠어",
                "강풍 경보래. 날아갈 뻔",
                "강풍 주의보야. 간판 조심해",
                "바람 폭탄이야. 외출 조심해"
            ],
            "건조": [
                "건조 특보야. 불조심해",
                "건조 경보래. 화재 위험해",
                "건조 주의보야. 물 많이 마셔",
                "습도 완전 낮아. 입술 갈라질 듯"
            ]
        }

        # 온도 및 기타 변수들
        temp_max = weather.get('temp_max', 0)
        temp_min = weather.get('temp_min', 0)
        temp_diff = weather.get('temp_diff', 0)
        rain_prob = weather.get('rain_prob_max', 0)
        wind_speed = weather.get('max_wind_speed', 0)
        humidity = weather.get('avg_humidity', 0)
        diurnal_range = weather.get('diurnal_range', 0)
        rain_amount = weather.get('total_rain_amount', 0)
        
        # **키 이름 수정**: main_weather → weather, temperature_state → temperature
        main_weather = weather.get('weather')  # 수정됨
        temperature_state = weather.get('temperature')  # 수정됨
        
        # 불쾌지수 관련 변수 추가
        discomfort_index = weather.get('discomfort_index')
        discomfort_level = weather.get('discomfort_level')

        # 0순위: 템플릿으로 처리되는 주요 특보 (HEATWAVE, HEAVY_RAIN, TYPHOON)
        # 이 경우, 템플릿 자체가 메시지이므로 별도의 캐치프레이즈를 생성하지 않습니다.        
        if main_weather in ['HEATWAVE', 'HEAVY_RAIN', 'TYPHOON']:
            print(f"[캐치프레이즈] 주요 특보로 인해 빈 문자열 반환: {main_weather}")
            return "" # 빈 문자열을 반환하여 캐치프레이즈 없앰

        # 1순위: 템플릿으로 처리되지 않는 기타 특보
        if warnings:
            warn_type = warnings.get('type')
            if warn_type in self.warning_phrases:
                selected_phrase = random.choice(self.warning_phrases[warn_type])
                print(f"[캐치프레이즈] 기타 특보: {warn_type} → '{selected_phrase}'")
                return selected_phrase

        # 1순위: 놓치기 아쉬운 특별한 날
        # 보름달 + 맑은 밤
        if (weather.get('night_sky_clarity') == '매우 맑음' and 
            astro.get('moon_phase_simple') == 'Full Moon'):
            selected_phrase = random.choice(self.special_moon_phrases)
            print(f"[캐치프레이즈] 특별한 달밤 → '{selected_phrase}'")
            return selected_phrase
        
        # 완벽한 야외활동 조건 (더 엄격하게)
        am_grade = indices.get('activity_index_am', {}).get('grade', 'N/A')
        pm_grade = indices.get('activity_index_pm', {}).get('grade', 'N/A')
        
        # 조건: 오전/오후 모두 Excellent + 기본 날씨가 맑음 + 비 확률 낮음
        if (am_grade == 'Excellent' and 
            pm_grade == 'Excellent' and
            main_weather == 'SUNNY' and
            rain_prob < 30):
            selected_phrase = random.choice(self.perfect_weather_phrases)
            print(f"[캐치프레이즈] 완벽한 날씨 (맑고 둘 다 최상, 비확률:{rain_prob}%) → '{selected_phrase}'")
            return selected_phrase
        
        # 2순위: 건강 및 안전 직결 상황
        if temp_max is not None and temp_min is not None:
            
            # **우선순위 재정렬**: 불쾌지수를 더 높은 우선순위로 이동
            # 극심한 불쾌지수 (최우선) - 폭염 + 습도 조합
            if (discomfort_level == '매우 높음' and 
                temperature_state in ['EXTREME']):
                phrases = self.extreme_hot_humid_phrases.copy()
                if discomfort_index:
                    phrases.append(f"불쾌지수 {int(discomfort_index)}. 찜통이야")
                    phrases.append(f"더위+습기 콤보. 불쾌지수 {int(discomfort_index)}")
                selected_phrase = random.choice(phrases)
                print(f"[캐치프레이즈] 극심한 불쾌지수 (레벨: {discomfort_level}, 지수: {discomfort_index}) → '{selected_phrase}'")
                return selected_phrase
            
            # 극한 추위 + 강풍 
            if (temperature_state == 'VERY_COLD' and 
                weather.get('wind_strength') in ['강한바람', '강풍']):
                selected_phrase = random.choice(self.extreme_cold_wind_phrases)
                print(f"[캐치프레이즈] 극한 추위+강풍 → '{selected_phrase}'")
                return selected_phrase
            
            # 강한 바람 + 비 
            if (weather.get('rain_prob_max', 0) >= 60 and 
                weather.get('wind_strength') in ['강한바람', '강풍']):
                selected_phrase = random.choice(self.rain_wind_phrases)
                print(f"[캐치프레이즈] 비바람 (비확률: {rain_prob}%) → '{selected_phrase}'")
                return selected_phrase
            
            # 전날 대비 급격한 기온 변화
            if temp_diff is not None:
                if temp_diff < -10:  # 갑자기 추워짐
                    phrases = self.temp_drop_phrases.copy()
                    phrases.append(f"어제보다 {abs(int(temp_diff))}도 떨어졌어. 감기 조심해")
                    selected_phrase = random.choice(phrases)
                    print(f"[캐치프레이즈] 급격한 기온 하락 ({temp_diff}도) → '{selected_phrase}'")
                    return selected_phrase
                elif temp_diff > 10:  # 갑자기 더워짐
                    phrases = self.temp_rise_phrases.copy()
                    phrases.append(f"어제보다 {int(temp_diff)}도 올랐어. 옷 벗어")
                    selected_phrase = random.choice(phrases)
                    print(f"[캐치프레이즈] 급격한 기온 상승 ({temp_diff}도) → '{selected_phrase}'")
                    return selected_phrase
            
            # 극한 더위 - 기본
            if temperature_state == 'EXTREME':  # 수정됨
                phrases = self.extreme_hot_phrases.copy()
                phrases.extend([
                    f"오늘 진짜 더워. {int(temp_max)}도래",
                    f"완전 더울 것 같아. {int(temp_max)}도까지",
                    f"더위 조심해. {int(temp_max)}도 넘어",
                    f"그늘에 있어. {int(temp_max)}도까지 올라가"
                ])
                selected_phrase = random.choice(phrases)
                print(f"[캐치프레이즈] 극한 더위 (온도상태: {temperature_state}, {temp_max}도) → '{selected_phrase}'")
                return selected_phrase
            
            # 극한 추위 - 기본
            if temperature_state == 'VERY_COLD':  # 수정됨
                phrases = self.extreme_cold_phrases.copy() 
                phrases.extend([
                    f"오늘 진짜 추워. 최저 {int(temp_min)}도",
                    f"추위 조심해. {int(temp_min)}도까지",
                    f"얼어 죽을 것 같아. {int(temp_min)}도래",
                    f"덜덜 떨겠어. {int(temp_min)}도"
                ])
                selected_phrase = random.choice(phrases)
                print(f"[캐치프레이즈] 극한 추위 (온도상태: {temperature_state}, {temp_min}도) → '{selected_phrase}'")
                return selected_phrase

        # 미세먼지 나쁨
        pm10_status = indices.get('air_quality_pm10', {}).get('status')
        pm25_status = indices.get('air_quality_pm25', {}).get('status')
        if pm10_status in ['Bad', 'Very Bad'] or pm25_status in ['Bad', 'Very Bad']:
            selected_phrase = random.choice(self.dust_phrases)
            print(f"[캐치프레이즈] 미세먼지 나쁨 (PM10: {pm10_status}, PM2.5: {pm25_status}) → '{selected_phrase}'")
            return selected_phrase
        
        # 높은 UV 지수 (우선순위 낮춤 - 불쾌지수 다음으로)
        uv_index = indices.get('uv_index') or 0
        if uv_index >= 8:  # UV 지수 8 이상 (Very High)
            phrases = self.high_uv_phrases.copy()
            phrases.append(f"UV 지수 {int(uv_index)}. 선크림 필수")
            selected_phrase = random.choice(phrases)
            print(f"[캐치프레이즈] 높은 UV 지수 ({uv_index}) → '{selected_phrase}'")
            return selected_phrase
        
        # 강한 비 - 강우량 많은 경우
        if (weather.get('total_rain_amount', 0) > 10 and 
            weather.get('rain_prob_max', 0) >= 70):
            phrases = self.heavy_rain_phrases.copy()
            phrases.append(f"비 진짜 많이 올 거야. {int(rain_amount)}mm 예상")
            selected_phrase = random.choice(phrases)
            print(f"[캐치프레이즈] 강한 비 (강우량: {rain_amount}mm, 확률: {rain_prob}%) → '{selected_phrase}'")
            return selected_phrase
        
        # 강한 비 - 확률만 높은 경우
        if weather.get('rain_prob_max', 0) >= 70:
            phrases = self.rain_high_prob_phrases.copy()
            phrases.extend([
                f"비 많이 올 확률 높아. {int(rain_prob)}%",
                f"비 확률 {int(rain_prob)}%. 우산 필수"
            ])
            selected_phrase = random.choice(phrases)
            print(f"[캐치프레이즈] 높은 비 확률 ({rain_prob}%) → '{selected_phrase}'")
            return selected_phrase
        
        # 열대야 - 계절별 (초여름/늦여름만)
        if temp_min is not None:
            month = date_obj.month
            if (temp_min > 25 and 
                month in [5, 6, 9]):  # 5-6월, 9월만
                phrases = self.tropical_night_phrases.copy()
                phrases.extend([
                    f"열대야네. 밤 기온 {int(temp_min)}도래",
                    f"밤에도 {int(temp_min)}도 넘을 거래. 더워"
                ])
                selected_phrase = random.choice(phrases)
                print(f"[캐치프레이즈] 열대야 ({month}월, 최저기온: {temp_min}도) → '{selected_phrase}'")
                return selected_phrase
        
        # 강한 바람 - 단독
        if weather.get('wind_strength') in ['강한바람', '강풍']:
            phrases = self.strong_wind_phrases.copy()
            phrases.append(f"바람 진짜 세게 불어. {wind_speed}m/s")
            selected_phrase = random.choice(phrases)
            print(f"[캐치프레이즈] 강한 바람 ({weather.get('wind_strength')}, {wind_speed}m/s) → '{selected_phrase}'")
            return selected_phrase
        
        # 큰 일교차
        if diurnal_range is not None and diurnal_range > 15:
            phrases = self.large_temp_diff_phrases.copy()
            phrases.append(f"일교차 심해. {int(diurnal_range)}도 차이")
            selected_phrase = random.choice(phrases)
            print(f"[캐치프레이즈] 큰 일교차 ({diurnal_range}도) → '{selected_phrase}'")
            return selected_phrase
        
        # 3순위: 일상적인 날씨 정보
        if main_weather == 'SUNNY':
            phrases = self.sunny_phrases.copy()
            phrases.append(f"오늘 날씨 맑아. 최고 {int(temp_max)}도")
            selected_phrase = random.choice(phrases)
            print(f"[캐치프레이즈] 맑은 날씨 → '{selected_phrase}'")
            return selected_phrase
        elif main_weather == 'HEATWAVE':  # HEATWAVE 케이스 추가
            phrases = self.extreme_hot_phrases.copy()
            phrases.append(f"폭염 주의보야. {int(temp_max)}도")
            selected_phrase = random.choice(phrases)
            print(f"[캐치프레이즈] 폭염 특보 → '{selected_phrase}'")
            return selected_phrase
        elif main_weather == 'CLOUDY':
            phrases = self.cloudy_phrases.copy()
            phrases.append(f"하늘 좀 흐리네. 최고 {int(temp_max)}도")
            selected_phrase = random.choice(phrases)
            print(f"[캐치프레이즈] 흐린 날씨 → '{selected_phrase}'")
            return selected_phrase
        elif main_weather == 'PARTLY_CLOUDY':
            phrases = self.partly_cloudy_phrases.copy()
            phrases.append(f"구름 조금 끼었어. 최고 {int(temp_max)}도")
            selected_phrase = random.choice(phrases)
            print(f"[캐치프레이즈] 부분 흐림 → '{selected_phrase}'")
            return selected_phrase
        elif main_weather == 'RAINY':
            phrases = self.rainy_phrases.copy()
            phrases.append(f"비 와. 확률 {int(rain_prob)}%")
            selected_phrase = random.choice(phrases)
            print(f"[캐치프레이즈] 비 오는 날씨 → '{selected_phrase}'")
            return selected_phrase
        elif main_weather == 'SNOW':
            phrases = self.snow_phrases.copy()
            phrases.append(f"눈 온대. 최저 {int(temp_min)}도")
            selected_phrase = random.choice(phrases)
            print(f"[캐치프레이즈] 눈 오는 날씨 → '{selected_phrase}'")
            return selected_phrase
        elif main_weather == 'SHOWER':
            phrases = self.shower_phrases.copy()
            phrases.append(f"소나기 온다고 해. {int(rain_prob)}% 확률")
            selected_phrase = random.choice(phrases)
            print(f"[캐치프레이즈] 소나기 → '{selected_phrase}'")
            return selected_phrase
        
        # 기온 상태별 (키 이름 수정됨)
        if temperature_state == 'HOT':
            phrases = self.hot_phrases.copy()
            phrases.extend([
                f"오늘 더울 것 같아. {int(temp_max)}도까지",
                f"온도 좀 높아. {int(temp_max)}도까지 올라가", 
                f"{int(temp_max)}도래. 좀 더울 것 같아"
            ])
            selected_phrase = random.choice(phrases)
            print(f"[캐치프레이즈] 더운 날씨 (온도상태: {temperature_state}) → '{selected_phrase}'")
            return selected_phrase
        elif temperature_state == 'COLD':
            phrases = self.cold_phrases.copy()
            phrases.append(f"좀 쌀쌀해. 최저 {int(temp_min)}도")
            selected_phrase = random.choice(phrases)
            print(f"[캐치프레이즈] 추운 날씨 (온도상태: {temperature_state}) → '{selected_phrase}'")
            return selected_phrase
        elif temperature_state == 'NORMAL':
            phrases = self.normal_temp_phrases.copy()
            phrases.append(f"날씨 적당해. 최고 {int(temp_max)}도")
            selected_phrase = random.choice(phrases)
            print(f"[캐치프레이즈] 적당한 날씨 (온도상태: {temperature_state}) → '{selected_phrase}'")
            return selected_phrase
        
        # 비 확률
        rain_prob = weather.get('rain_prob_max', 0)
        if 30 <= rain_prob <= 60:
            phrases = self.light_rain_phrases.copy()
            phrases.extend([
                f"비 올 수도 있어. {int(rain_prob)}% 확률",
                f"비 확률 {int(rain_prob)}%. 애매하네"
            ])
            selected_phrase = random.choice(phrases)
            print(f"[캐치프레이즈] 애매한 비 확률 ({rain_prob}%) → '{selected_phrase}'")
            return selected_phrase
        
        # 기본값
        selected_phrase = random.choice(self.normal_temp_phrases)
        print(f"[캐치프레이즈] 기본값 (적당한 날씨) → '{selected_phrase}'")
        return selected_phrase
