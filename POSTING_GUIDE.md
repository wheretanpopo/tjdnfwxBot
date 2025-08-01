### 인스타그램 공지 포스트 내용

#### **[한국어 버전]**

**[제목] 안녕하세요! 서울의 날씨를 알려드리는 채널입니다.**

**[본문]**
이 계정은 매일 아침, 대한민국 공공 데이터를 활용해 서울의 최신 날씨 정보를 자동으로 알려드리는 채널입니다.

오늘의 날씨, 기온, 미세먼지, 자외선 지수뿐만 아니라, 외부 활동에 도움이 되는 '야외 활동 지수'까지 한눈에 확인하실 수 있습니다.

모든 정보는 기상청, 에어코리아, 천문연구원의 공식 데이터를 기반으로 생성됩니다.

매일 아침, 가장 정확하고 유용한 날씨 정보로 찾아뵙겠습니다.
감사합니다!

**[해시태그]**
`#날씨 #서울날씨 #자동업데이트 #기상청 #에어코리아 #오늘의날씨 #정보`

---

#### **[English Version]**

**[Title] Welcome! This is your daily guide to Seoul's weather.**

**[Body]**
This account automatically posts the latest weather information for Seoul every morning, using public data from South Korea.

You can check today's weather, temperature, fine dust levels, UV index, and even an "Outdoor Activity Index" to help you plan your day.

All information is generated based on official data from the KMA (Korea Meteorological Administration), Air Korea, and KASI.

We'll be back every morning with the most accurate and helpful weather updates.
Thank you!

**[Hashtags]**
`#Weather #SeoulWeather #DailyUpdate #KMA #AirKorea #TodaysWeather #Info`

---

### 날씨 데이터 처리 및 이미지 생성 기준

| 항목 | 데이터 소스 | 판단 기준 |
| :--- | :--- | :--- |
| **날씨 아이콘/템플릿** | 기상청 단기예보 | **하늘상태(SKY)** 코드와 **강수형태(PTY)** 코드를 조합하여 결정<br>- **맑음(Sunny)**: SKY(1)<br>- **구름많음(Cloudy)**: SKY(3, 4)<br>- **비(Rainy)**: PTY(1, 2, 4)<br>- **눈(Snowy)**: PTY(3) |
| **기온** | 기상청 단기예보 | - **오늘의 최고/최저 기온** 표시<br>- 어제 최고 기온과 비교하여 `어제보다 N° 높아요/낮아요` 문구 생성 |
| **미세먼지 (PM10/PM2.5)** | 에어코리아 대기질 예보 | **통합대기환경지수** 기준<br>- **좋음**: PM10(0~30), PM2.5(0~15)<br>- **보통**: PM10(31~80), PM2.5(16~35)<br>- **나쁨**: PM10(81~150), PM2.5(36~75)<br>- **매우나쁨**: PM10(151~), PM2.5(76~) |
| **자외선 지수 (UV)** | 한국천문연구원 생활기상지수 | **자외선 B(UVB) 지수** 기준<br>- **낮음 (1~2)**: 안전<br>- **보통 (3~5)**: 2-3시간 노출 시 피부 화상 가능<br>- **높음 (6~7)**: 1-2시간 노출 시 피부 화상 가능<br>- **매우높음 (8~10)**: 수십 분 내 피부 화상 가능<br>- **위험 (11 이상)**: 즉시 피부 화상 가능 |
| **기상 특보** | 기상청 기상특보 | 발표된 특보 중 아래 항목에 해당하는 경우 특별 템플릿 사용<br>- **폭염**: 폭염주의보/경보<br>- **호우**: 호우주의보/경보<br>- **태풍**: 태풍주의보/경보 |
| **야외 활동 지수** | 자체 개발 로직 | **날씨, 기온, UV, 미세먼지**를 종합하여 5단계로 평가<br>- **최상(Best)**: 맑고, 기온 적절, UV 낮음, 미세먼지 좋음<br>- **좋음(Good)**: 구름 조금, 기온 무난, UV 보통, 미세먼지 보통<br>- **보통(Normal)**: 흐림, 약간 덥거나 추움, UV 높음, 미세먼지 보통<br>- **나쁨(Bad)**: 비/눈 소식, 덥거나 추움, UV 매우높음, 미세먼지 나쁨<br>- **최악(Worst)**: 기상 특보 발효, 극심한 더위/추위, 미세먼지 매우나쁨 |
| **오늘의 캐치프레이즈** | 자체 개발 로직 | 그날의 날씨 데이터를 종합하여 가장 두드러지는 특징을 요약한 문구 생성<br> (예: "화창하지만 자외선은 조심하세요!", "우산 꼭 챙겨야 하는 하루") |
