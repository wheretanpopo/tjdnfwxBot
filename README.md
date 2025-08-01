# MyFirstGeminiApp: 날씨 정보 기반 이미지 생성 및 공유 애플리케이션

## 프로젝트 개요
이 프로젝트는 기상청, 에어코리아, 한국천문연구원(KASI) 등의 공공 API를 활용하여 날씨, 미세먼지, 천문 정보를 수집하고, 이를 바탕으로 날씨 예보 이미지를 생성하는 애플리케이션입니다. 생성된 이미지는 소셜 미디어 등에 공유될 수 있도록 디자인되었습니다.

## 주요 기능
*   **날씨 정보 수집**: 기상청 API를 통해 현재 날씨 및 예보 정보를 가져옵니다.
*   **미세먼지 정보 수집**: 에어코리아 API를 통해 미세먼지 농도 정보를 가져옵니다.
*   **천문 정보 수집**: 한국천문연구원(KASI) API를 통해 일출/일몰 시각 등의 천문 정보를 가져옵니다.
*   **날씨 문구 생성**: 현재 날씨 상태에 맞는 다양한 문구를 생성합니다. (한국어 및 영어 지원)
*   **활동 지수 계산**: 날씨 데이터를 기반으로 외부 활동에 대한 지수를 계산합니다.
*   **이미지 생성**: 수집된 정보와 날씨 문구를 조합하여 시각적으로 매력적인 날씨 예보 이미지를 생성합니다.
*   **다국어 지원**: 한국어(`weather_phrases_ko.py`) 및 영어(`weather_phrases.py`) 날씨 문구를 지원합니다.

## 설치 및 실행 방법

### 1. Python 환경 설정
Python 3.8 이상이 설치되어 있어야 합니다.

### 2. 의존성 설치
`requirements.txt`에 명시된 라이브러리들을 설치합니다.
```bash
pip install -r requirements.txt
```

### 3. API 키 설정
`.env` 파일에 필요한 API 키들을 설정해야 합니다. `.env.txt` 파일을 참조하여 `.env` 파일을 생성하고 다음 변수들을 채워 넣으세요.
*   `KMA_API_KEY`: 기상청 API 키
*   `AIRKOREA_API_KEY`: 에어코리아 API 키
*   `KASI_API_KEY`: 한국천문연구원 API 키
*   `INSTAGRAM_ACCESS_TOKEN`: Instagram Graph API 액세스 토큰
*   `INSTAGRAM_USER_ID`: Instagram 사용자 ID
*   `IMGUR_CLIENT_ID`: Imgur API 클라이언트 ID

### 4. 애플리케이션 실행
`main.py` 파일을 실행하여 애플리케이션을 시작합니다.
```bash
python main.py
```
실행 시 `weather_service/output` 디렉토리에 날씨 예보 이미지가 생성되며, 설정된 인스타그램 계정에 자동으로 포스팅됩니다.

## Instagram API 연동
이 애플리케이션은 Instagram Graph API를 사용하여 생성된 날씨 이미지를 자동으로 포스팅합니다.

### 주요 기능
*   **캐러셀 포스팅**: 한국어와 영어 버전의 날씨 이미지를 하나의 캐러셀 포스트로 묶어 게시합니다.
*   **스토리 포스팅**: 생성된 한국어 버전의 날씨 이미지를 인스타그램 스토리에 게시합니다.
*   **동적 캡션 생성**: 날씨 데이터와 현재 날짜를 기반으로 포스트 캡션을 동적으로 생성합니다.
*   **Imgur 연동**: Instagram API의 제약 사항을 우회하기 위해, 이미지를 Imgur에 업로드하고 해당 이미지 URL을 사용하여 Instagram에 게시하는 방식을 사용합니다.

### 포스팅 전략
*   **매일 자동 포스팅**: `main.py` 실행 시 자동으로 인스타그램 포스팅이 진행됩니다.
*   **언어 우선순위**: 날짜가 홀수이면 한국어 이미지를, 짝수이면 영어 이미지를 캐러셀의 첫 번째 순서로 배치하여 포스팅합니다.
*   **스토리**: 매일 한국어 버전의 이미지를 스토리에 게시합니다.

## 프로젝트 구조
```
.
├── api_clients/             # 각종 외부 API 연동 모듈
│   ├── airkorea_api.py      # 에어코리아 API 클라이언트
│   ├── kasi_api.py          # 한국천문연구원 API 클라이언트
│   └── kma_api.py           # 기상청 API 클라이언트
├── weather_service/         # 날씨 서비스 관련 리소스 및 설정
│   ├── config/              # 설정 파일 (위치 정보, 마지막 데이터 등)
│   │   ├── last_day_data.json
│   │   └── positions.json   # 이미지 생성에 사용될 텍스트 위치 정보
│   ├── fonts/               # 이미지 생성에 사용될 폰트 파일
│   ├── output/              # 생성된 날씨 이미지 저장 경로
│   └── templates/           # 이미지 템플릿 및 관련 리소스
│       └── posts/           # 날씨별 이미지 템플릿
├── astro_processor.py       # 천문 데이터 처리 모듈
├── config.py                # 전역 설정 및 상수 정의
├── coordinate_test.py       # (개발용) 기상청 격자 좌표와 위경도 좌표 변환 테스트 스크립트
├── data_processor.py        # 수집된 날씨 데이터 처리 및 가공 모듈
├── forecast_generator.py    # 날씨 예보 문구 생성 및 종합 모듈
├── image_generator.py       # PIL(Pillow)을 이용한 날씨 이미지 생성 모듈
├── instagram_api.py         # Instagram API 연동 및 포스팅 모듈
├── main.py                  # 애플리케이션의 메인 진입점
├── outdoor_activity_index.py # 외부 활동 지수 계산 모듈
├── requirements.txt         # Python 의존성 목록
├── weather_phrases.py       # 영어 날씨 문구 정의
└── weather_phrases_ko.py    # 한국어 날씨 문구 정의
```


## 개발자 정보
@scrathy
