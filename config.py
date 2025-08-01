# config.py
# 애플리케이션의 주요 설정을 관리합니다.
import os
from dotenv import load_dotenv
from pathlib import Path

# GitHub Actions 환경인지 확인 (CI라는 환경 변수가 보통 설정됨)
IS_GITHUB_ACTIONS = os.getenv('CI') == 'true'

# 로컬 환경일 경우에만 .env 파일에서 환경 변수를 로드합니다.
if not IS_GITHUB_ACTIONS:
    project_dir = Path(__file__).parent
    dotenv_path = project_dir / '.env'
    load_dotenv(dotenv_path=dotenv_path)

# API 키 및 토큰을 환경 변수에서 가져옵니다.
# GitHub Actions에서는 Secrets을 통해, 로컬에서는 .env 파일을 통해 주입됩니다.
KMA_API_KEY = os.getenv("KMA_API_KEY")
AIRKOREA_API_KEY = os.getenv("AIRKOREA_API_KEY")
KASI_API_KEY = os.getenv("KASI_API_KEY")

INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
INSTAGRAM_USER_ID = os.getenv("INSTAGRAM_USER_ID")
IMGUR_CLIENT_ID = os.getenv("IMGUR_CLIENT_ID")

# 예보 위치 (서울)
SEOUL_NX = 60
SEOUL_NY = 127
SEOUL_AREA_ID = "1100000000" # 서울 지역 코드
