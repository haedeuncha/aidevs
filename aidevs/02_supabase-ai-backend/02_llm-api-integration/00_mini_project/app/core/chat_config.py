
from pathlib import Path

from dotenv import load_dotenv

# 상위폴더에 있는 파일을 끌어오는 코드
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")