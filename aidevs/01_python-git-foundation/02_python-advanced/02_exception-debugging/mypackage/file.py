
import json
from pathlib import Path


CURRENT_DIR = Path(__file__).parent

# json파일을 dict 형식으로 변환하여 파이썬에서 읽을수있게 도와주는 함수
def read_json_safely(file_name: str) -> dict:
    """JSON 파일을 읽고 dict로 반환합니다.

    오류가 나면 프로그램을 바로 종료하지 않고 빈 dict를 반환합니다.
    """

    file_path = CURRENT_DIR / file_name
    try:
        text = file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError("파일이 없습니다.")
    # json을 dict로 변환함
    try:
        return json.loads(text)
    except json.decoder.JSONDecodeError as error:
        raise error
