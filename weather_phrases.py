import random
from datetime import datetime

class WeatherPhraseGenerator:
    def __init__(self):
        # 1순위: 놓치기 아쉬운 특별한 날
        self.special_moon_phrases = [
            "Full moon tonight. Sky's super clear",
            "Full moon today. No clouds",
            "Full moon's up. Go check it out",
            "Moon's gonna be beautiful. It's full",
            "Perfect night for moon gazing",
            "Full moon night. Time to howl",
            "Clear skies and full moon. Perfect combo"
        ]
        
        self.perfect_weather_phrases = [
            "Perfect weather. Great day to go out",
            "Weather's amazing. Wanna go anywhere",
            "Perfect day for outdoor stuff",
            "Too nice to stay inside",
            "Weather gods blessed us today",
            "This weather should be illegal",
            "All conditions are absolutely perfect"
        ]
        
        # 2순위: 건강 및 안전 직결 상황
        self.temp_drop_phrases = [
            "Suddenly got chilly. Bundle up",
            "Temperature dropped big time. Be careful",
            "Way colder than yesterday. Didn't see this coming",
            "Yesterday was a lie. Suddenly freezing",
            "Temperature plunged. Layer up smart"
        ]
        
        self.temp_rise_phrases = [
            "Suddenly got hot. Dress light",
            "Temperature shot up. Summer's here",
            "Way hotter than yesterday. Surprised?",
            "Global warming hit overnight",
            "Temperature jumped. Don't be shocked"
        ]
        
        self.extreme_cold_wind_phrases = [
            "Freezing cold plus wind. Gonna freeze solid",
            "Below zero and windy. Super cold",
            "Cold plus wind. Stay inside",
            "Cold and windy. Feels even colder",
            "Wind making it feel like a freezer",
            "Extreme cold with gusts. Worst combo"
        ]
        
        # **불쾌지수 관련 문구 추가** (누락되어 있었음)
        self.extreme_hot_humid_phrases = [
            "Hot and humid. It's a sauna",
            "Hot and sticky. Humidity's maxed",
            "Heat plus humidity. AC time",
            "Sauna weather. Don't go out",
            "Sauna outside another sauna",
            "Heat and humidity's fantastic combo",
            "Muggy and hot. Stay hydrated",
            "Sticky heat. Feels way hotter",
            "Humid heat wave. AC is life",
            "Sweating just standing still"
        ]
        
        self.rain_wind_phrases = [
            "Rain and wind. Umbrella's useless",
            "Storm's coming. Stay inside",
            "Rain plus wind. Be careful out there",
            "Stormy weather. Umbrella will flip",
            "Umbrella's gonna break in 5 minutes",
            "Storm combo. Netflix at home instead"
        ]
        
        self.extreme_hot_phrases = [
            "Could fry eggs on pavement",
            "Scorching heat. AC's crying"
        ]
        
        self.extreme_cold_phrases = [
            "Super cold. Below freezing",
            "Freezing cold. Bundle up tight",
            "Polar vortex. Layer up",
            "Wanna hibernate under blankets"
        ]
        
        self.dust_phrases = [
            "Air quality's bad. Wear a mask",
            "Air's gross. Stay inside",
            "Dust levels high. Close windows",
            "Air quality sucks. Mask up",
            "Air's really bad. Be careful",
            "Breathing's a luxury today",
            "Air's not great today. Mask time"
        ]
        
        self.high_uv_phrases = [
            "UV's really strong. Sunscreen up",
            "UV index high. Use umbrella",
            "Sun's gonna be harsh. Wear a hat",
            "UV protection needed. Skin'll burn",
            "Sunshine's blazing. Stay in shade",
            "UV bomb today. Sunscreen essential",
            "UV so strong you'll burn in 5 minutes"
        ]
        
        self.heavy_rain_phrases = [
            "Heavy rain coming. Get ready",
            "Downpour alert. Stay inside",
            "Rain's gonna pour. Prepare",
            "Major rain incoming. Be careful",
            "Sky opened the faucet",
            "Heavy rain prep. Better stay home"
        ]
        
        self.rain_high_prob_phrases = [
            "High chance of rain. Bring umbrella",
            "Likely to rain. Get ready",
            "Rain's probable. Umbrella time",
            "Gonna rain. Prepare",
            "Sky's ready to cry",
            "Pretty sure it's gonna rain"
        ]
        
        self.tropical_night_phrases = [
            "Hot night already. Gonna be warm",
            "Late tropical night. Still hot in September",
            "Early tropical night. Check your AC"
        ]
        
        self.strong_wind_phrases = [
            "Super windy. Hold onto your hat",
            "Windy day. Hat might fly off",
            "Strong winds coming. Stay safe",
            "Really windy. Watch light stuff",
            "Strong wind alert. Be careful",
            "Wind's giving free natural perms",
            "Gusty winds. Watch the signs"
        ]
        
        self.large_temp_diff_phrases = [
            "Big temp swing. Cold morning, hot afternoon",
            "Temperature gap's huge. Layer up",
            "Morning's cold, afternoon's hot",
            "Big temp difference. Dress smart",
            "Chilly morning, warm afternoon",
            "Temperature's on a roller coaster",
            "Outfit choice nightmare day"
        ]
        
        # 3순위: 일상적인 날씨 정보
        self.sunny_phrases = [
            "Sun's amazing. Feels good",
            "Super sunny day. Perfect for laundry",
            "Sunshine's gorgeous today",
            "Beautiful sunny day. Great for walks",
            "Clear skies. Mood's gonna lift",
            "Weather matches my mood perfectly",
            "Sun's doing its service"
        ]
        
        self.cloudy_phrases = [
            "Bit cloudy today. Still okay though",
            "Lots of clouds. Gonna be cool",
            "Overcast day. Calm vibes",
            "Clouds covering everything",
            "Sky's all gray today",
            "Cloudy but no rain expected",
            "Sky looks moody. Just like me",
            "Clouds conquered the sky"
        ]
        
        self.partly_cloudy_phrases = [
            "Some clouds around. Just right",
            "Half cloudy sky. Nice weather",
            "Clouds here and there. Not bad",
            "Sun peeking through clouds. Pretty",
            "Partly cloudy day. Just right",
            "Some clouds but still sunny",
            "Clouds being lazy. Stopped halfway",
            "Clouds and sun playing tug of war"
        ]
        
        self.hot_phrases = [
            "Getting warm. Dress light",
            "Bit of heat coming. Get ready",
            "Temperature's rising. Dress cool",
            "Getting warmer. Light clothes",
            "Warm side of comfortable",
            "AC's not being dramatic anymore"
        ]
        
        self.cold_phrases = [
            "Bit chilly. Light jacket time",
            "Cool day. Layer up lightly",
            "Little cold today. Bundle up",
            "Thin cardigan weather",
            "Getting chilly. Watch out for colds",
            "Bit cool today. Dress warm",
            "Little cold. Stay warm",
            "Chilly weather. Stay healthy",
            "Getting cool. Watch for colds",
            "Bit cold. Keep warm",
            "Autumn's sneaking in"
        ]
        
        self.normal_temp_phrases = [
            "Weather's just right. Great day out",
            "Temperature's perfect. So comfy",
            "Weather's nice. No outfit worries",
            "Weather's cozy. Feels good",
            "Temperature's spot on. So nice",
            "Weather's perfect for anything",
            "Weather's peaceful. Relaxing day",
            "Temperature's great. Perfect for activities",
            "Goldilocks would love this weather"
        ]
        
        self.light_rain_phrases = [
            "Might rain. Bring umbrella",
            "Rain or no rain. Who knows",
            "Light rain possible",
            "Better carry umbrella around",
            "Some rain expected. Be ready",
            "Just in case, bring umbrella",
            "Light rain might happen",
            "50/50 rain. Should I bring umbrella?"
        ]
        
        self.rainy_phrases = [
            "It's raining. Bring umbrella for sure",
            "Rain's coming. Get ready",
            "Gonna rain today. Bring umbrella",
            "Rain's falling. Stay dry",
            "Rain alert. Umbrella's a must",
            "Rain today. Be prepared",
            "Rain's coming. Don't get soaked",
            "Rain expected. Bring umbrella",
            "Sky's crying. Bring umbrella"
        ]
        
        self.snow_phrases = [
            "Snow's coming. Don't slip",
            "Gonna snow. Drive carefully",
            "Snow today. Watch your step",
            "Snow alert. Roads might be slick",
            "Snow's falling. Be careful",
            "Snow expected. Don't fall",
            "Snow today. Bundle up",
            "Snow's coming. Drive safe",
            "Sky's dropping cotton candy"
        ]
        
        self.shower_phrases = [
            "Showers expected",
            "Shower alert. Bring umbrella",
            "Sudden rain possible",
            "Showers might happen",
            "Quick rain expected",
            "Sudden showers possible",
            "High shower chance",
            "Brief rain expected",
            "Sky's planning a surprise cry"
        ]

        # 특보별 캐치프레이즈 (템플릿이 없는 특보용)
        self.warning_phrases = {
            "한파": [
                "Cold wave warning. Gonna freeze",
                "Cold front alert. Bundle up tight",
                "Extreme cold warning. Stay warm",
                "Freeze warning. Layer up"
            ],
            "대설": [
                "Heavy snow warning. Roads dangerous",
                "Snow storm alert. Stay inside",
                "Blizzard warning. Drive carefully",
                "Heavy snowfall alert. Watch your step"
            ],
            "강풍": [
                "Strong wind warning. Hold tight",
                "Wind storm alert. Stay safe",
                "Gale warning. Secure loose items",
                "High wind alert. Be careful outside"
            ],
            "건조": [
                "Dry conditions warning. Fire risk high",
                "Drought alert. Stay hydrated",
                "Low humidity warning. Moisturize",
                "Dry air alert. Fire danger"
            ]
        }

    def generate_phrase(self, final_data):
        weather = final_data.get('weather_summary', {})
        indices = final_data.get('indices', {})
        astro = final_data.get('astro_info', {})
        warnings = final_data.get('warnings')
        info = final_data.get('info', {})
        date_obj = info.get('date_object')

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
            print(f"[Catchphrase] Major warning - returning empty string: {main_weather}")
            return "" # 빈 문자열을 반환하여 캐치프레이즈 없앰

        # 1순위: 템플릿으로 처리되지 않는 기타 특보
        if warnings:
            warn_type = warnings.get('type')
            if warn_type in self.warning_phrases:
                selected_phrase = random.choice(self.warning_phrases[warn_type])
                print(f"[Catchphrase] Other warning: {warn_type} → '{selected_phrase}'")
                return selected_phrase

        # 1순위: 놓치기 아쉬운 특별한 날
        # 보름달 + 맑은 밤
        if (weather.get('night_sky_clarity') == '매우 맑음' and 
            astro.get('moon_phase_simple') == 'Full Moon'):
            selected_phrase = random.choice(self.special_moon_phrases)
            print(f"[Catchphrase] Special moon night → '{selected_phrase}'")
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
            print(f"[Catchphrase] Perfect weather (sunny & both excellent, rain prob:{rain_prob}%) → '{selected_phrase}'")
            return selected_phrase
        
        # 2순위: 건강 및 안전 직결 상황
        if temp_max is not None and temp_min is not None:
            
            # **우선순위 재정렬**: 불쾌지수를 더 높은 우선순위로 이동
            # 극심한 불쾌지수 (최우선) - 폭염 + 습도 조합
            if (discomfort_level == '매우 높음' and 
                temperature_state in ['EXTREME', 'VERY_HOT']):
                phrases = self.extreme_hot_humid_phrases.copy()
                if discomfort_index:
                    phrases.append(f"Discomfort index {int(discomfort_index)}. Sauna outside")
                    phrases.append(f"Heat+humidity combo. Discomfort {int(discomfort_index)}")
                selected_phrase = random.choice(phrases)
                print(f"[Catchphrase] Extreme discomfort (level: {discomfort_level}, index: {discomfort_index}) → '{selected_phrase}'")
                return selected_phrase
            
            # 극한 추위 + 강풍 
            if (temperature_state == 'VERY_COLD' and 
                weather.get('wind_strength') in ['강한바람', '강풍']):
                selected_phrase = random.choice(self.extreme_cold_wind_phrases)
                print(f"[Catchphrase] Extreme cold + wind → '{selected_phrase}'")
                return selected_phrase
            
            # 강한 바람 + 비 
            if (weather.get('rain_prob_max', 0) >= 60 and 
                weather.get('wind_strength') in ['강한바람', '강풍']):
                selected_phrase = random.choice(self.rain_wind_phrases)
                print(f"[Catchphrase] Rain + wind (rain prob: {rain_prob}%) → '{selected_phrase}'")
                return selected_phrase
            
            # 전날 대비 급격한 기온 변화
            if temp_diff is not None:
                if temp_diff < -10:  # 갑자기 추워짐
                    phrases = self.temp_drop_phrases.copy()
                    phrases.append(f"{abs(int(temp_diff))}°C colder than yesterday. Stay warm")
                    selected_phrase = random.choice(phrases)
                    print(f"[Catchphrase] Sharp temp drop ({temp_diff}°C) → '{selected_phrase}'")
                    return selected_phrase
                elif temp_diff > 10:  # 갑자기 더워짐
                    phrases = self.temp_rise_phrases.copy()
                    phrases.append(f"{int(temp_diff)}°C warmer than yesterday. Strip down")
                    selected_phrase = random.choice(phrases)
                    print(f"[Catchphrase] Sharp temp rise ({temp_diff}°C) → '{selected_phrase}'")
                    return selected_phrase
            
            # 극한 더위 - 기본
            if temperature_state == 'EXTREME':  # 수정됨
                phrases = self.extreme_hot_phrases.copy()
                phrases.extend([
                    f"Really hot today. {int(temp_max)}°C",
                    f"Super hot. Up to {int(temp_max)}°C",
                    f"Heat wave. {int(temp_max)}°C, stay in shade",
                    f"Really hot. {int(temp_max)}°C today"
                ])
                selected_phrase = random.choice(phrases)
                print(f"[Catchphrase] Extreme heat (temp state: {temperature_state}, {temp_max}°C) → '{selected_phrase}'")
                return selected_phrase
            
            # 극한 추위 - 기본
            if temperature_state == 'VERY_COLD':  # 수정됨
                phrases = self.extreme_cold_phrases.copy() 
                phrases.extend([
                    f"Really cold today. {int(temp_min)}°C",
                    f"Super cold. Down to {int(temp_min)}°C",
                    f"Freezing cold. {int(temp_min)}°C, bundle up tight",
                    f"Polar vortex. {int(temp_min)}°C today",
                    f"Freezing my butt off. {int(temp_min)}°C",
                    f"Shivering cold. {int(temp_min)}°C"
                ])
                selected_phrase = random.choice(phrases)
                print(f"[Catchphrase] Extreme cold (temp state: {temperature_state}, {temp_min}°C) → '{selected_phrase}'")
                return selected_phrase

        # 미세먼지 나쁨
        pm10_status = indices.get('air_quality_pm10', {}).get('status')
        pm25_status = indices.get('air_quality_pm25', {}).get('status')
        if pm10_status in ['Bad', 'Very Bad'] or pm25_status in ['Bad', 'Very Bad']:
            selected_phrase = random.choice(self.dust_phrases)
            print(f"[Catchphrase] Bad air quality (PM10: {pm10_status}, PM2.5: {pm25_status}) → '{selected_phrase}'")
            return selected_phrase
        
        # 높은 UV 지수 (우선순위 낮춤 - 불쾌지수 다음으로)
        uv_index = indices.get('uv_index') or 0
        if uv_index >= 8:  # UV 지수 8 이상 (Very High)
            phrases = self.high_uv_phrases.copy()
            phrases.append(f"UV index {int(uv_index)}. Sunscreen essential")
            selected_phrase = random.choice(phrases)
            print(f"[Catchphrase] High UV index ({uv_index}) → '{selected_phrase}'")
            return selected_phrase
        
        # 강한 비 - 강우량 많은 경우
        if (weather.get('total_rain_amount', 0) > 10 and 
            weather.get('rain_prob_max', 0) >= 70):
            phrases = self.heavy_rain_phrases.copy()
            phrases.append(f"Heavy rain coming. {int(rain_amount)}mm expected")
            selected_phrase = random.choice(phrases)
            print(f"[Catchphrase] Heavy rain (amount: {rain_amount}mm, prob: {rain_prob}%) → '{selected_phrase}'")
            return selected_phrase
        
        # 강한 비 - 확률만 높은 경우
        if weather.get('rain_prob_max', 0) >= 70:
            phrases = self.rain_high_prob_phrases.copy()
            phrases.extend([
                f"High chance of rain. {int(rain_prob)}%",
                f"{int(rain_prob)}% rain chance. Umbrella's a must"
            ])
            selected_phrase = random.choice(phrases)
            print(f"[Catchphrase] High rain probability ({rain_prob}%) → '{selected_phrase}'")
            return selected_phrase
        
        # 열대야 - 계절별 (초여름/늦여름만)
        if temp_min is not None:
            month = date_obj.month
            if (temp_min > 25 and 
                month in [5, 6, 9]):  # 5-6월, 9월만
                phrases = self.tropical_night_phrases.copy()
                phrases.extend([
                    f"Tropical night early. {int(temp_min)}°C at night",
                    f"Night stays hot. Over {int(temp_min)}°C",
                    f"Night's {int(temp_min)}°C. Our electric bill's dead"
                ])
                selected_phrase = random.choice(phrases)
                print(f"[Catchphrase] Tropical night ({month}월, min temp: {temp_min}°C) → '{selected_phrase}'")
                return selected_phrase
        
        # 강한 바람 - 단독
        if weather.get('wind_strength') in ['강한바람', '강풍']:
            phrases = self.strong_wind_phrases.copy()
            phrases.append(f"Super windy. {wind_speed}m/s gusts")
            selected_phrase = random.choice(phrases)
            print(f"[Catchphrase] Strong wind ({weather.get('wind_strength')}, {wind_speed}m/s) → '{selected_phrase}'")
            return selected_phrase
        
        # 큰 일교차
        if diurnal_range is not None and diurnal_range > 15:
            phrases = self.large_temp_diff_phrases.copy()
            phrases.append(f"Big temp swing. {int(diurnal_range)}°C difference")
            selected_phrase = random.choice(phrases)
            print(f"[Catchphrase] Large diurnal range ({diurnal_range}°C) → '{selected_phrase}'")
            return selected_phrase
        
        # 3순위: 일상적인 날씨 정보
        if main_weather == 'SUNNY':
            phrases = self.sunny_phrases.copy()
            phrases.append(f"Weather's clear today. High {int(temp_max)}°C")
            selected_phrase = random.choice(phrases)
            print(f"[Catchphrase] Sunny weather → '{selected_phrase}'")
            return selected_phrase
        elif main_weather == 'HEATWAVE':  # HEATWAVE 케이스 추가
            phrases = self.extreme_hot_phrases.copy()
            phrases.append(f"Heat wave alert. {int(temp_max)}°C")
            selected_phrase = random.choice(phrases)
            print(f"[Catchphrase] Heat wave → '{selected_phrase}'")
            return selected_phrase
        elif main_weather == 'CLOUDY':
            phrases = self.cloudy_phrases.copy()
            phrases.append(f"Bit cloudy today. High {int(temp_max)}°C")
            selected_phrase = random.choice(phrases)
            print(f"[Catchphrase] Cloudy weather → '{selected_phrase}'")
            return selected_phrase
        elif main_weather == 'PARTLY_CLOUDY':
            phrases = self.partly_cloudy_phrases.copy()
            phrases.append(f"Some clouds around. High {int(temp_max)}°C")
            selected_phrase = random.choice(phrases)
            print(f"[Catchphrase] Partly cloudy → '{selected_phrase}'")
            return selected_phrase
        elif main_weather == 'RAINY':
            phrases = self.rainy_phrases.copy()
            phrases.append(f"It's raining. {int(rain_prob)}% chance")
            selected_phrase = random.choice(phrases)
            print(f"[Catchphrase] Rainy weather → '{selected_phrase}'")
            return selected_phrase
        elif main_weather == 'SNOW':
            phrases = self.snow_phrases.copy()
            phrases.append(f"Snow's coming. Low {int(temp_min)}°C")
            selected_phrase = random.choice(phrases)
            print(f"[Catchphrase] Snowy weather → '{selected_phrase}'")
            return selected_phrase
        elif main_weather == 'SHOWER':
            phrases = self.shower_phrases.copy()
            phrases.append(f"Showers expected. {int(rain_prob)}% chance")
            selected_phrase = random.choice(phrases)
            print(f"[Catchphrase] Showers → '{selected_phrase}'")
            return selected_phrase
        
        # 기온 상태별 (키 이름 수정됨)
        if temperature_state == 'HOT':
            phrases = self.hot_phrases.copy()
            phrases.extend([
                f"Gonna be hot today. {int(temp_max)}°C",
                f"Getting warm. {int(temp_max)}°C today",
                f"{int(temp_max)}°C today. Gonna be warm"
            ])
            selected_phrase = random.choice(phrases)
            print(f"[Catchphrase] Hot weather (temp state: {temperature_state}) → '{selected_phrase}'")
            return selected_phrase
        elif temperature_state == 'COLD':
            phrases = self.cold_phrases.copy()
            phrases.append(f"Bit chilly. Low {int(temp_min)}°C")
            selected_phrase = random.choice(phrases)
            print(f"[Catchphrase] Cold weather (temp state: {temperature_state}) → '{selected_phrase}'")
            return selected_phrase
        elif temperature_state == 'NORMAL':
            phrases = self.normal_temp_phrases.copy()
            phrases.append(f"Weather's just right. High {int(temp_max)}°C")
            selected_phrase = random.choice(phrases)
            print(f"[Catchphrase] Normal weather (temp state: {temperature_state}) → '{selected_phrase}'")
            return selected_phrase
        
        # 비 확률
        rain_prob = weather.get('rain_prob_max', 0)
        if 30 <= rain_prob <= 60:
            phrases = self.light_rain_phrases.copy()
            phrases.extend([
                f"Might rain. {int(rain_prob)}% chance",
                f"{int(rain_prob)}% rain chance. Kinda iffy"
            ])
            selected_phrase = random.choice(phrases)
            print(f"[Catchphrase] Light rain probability ({rain_prob}%) → '{selected_phrase}'")
            return selected_phrase
        
        # 기본값
        selected_phrase = random.choice(self.normal_temp_phrases)
        print(f"[Catchphrase] Default (normal weather) → '{selected_phrase}'")
        return selected_phrase