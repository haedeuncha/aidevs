r"""JSON 파일을 안전하게 읽는 예제입니다.

실행 위치:
    C:\aidev\01_python-git-foundation

실행 명령:
    python .\02_python-advanced\02_exception-debugging\03_read_json_safely.py

이 예제의 목표:
    1. JSON 파일을 읽습니다.
    2. 파일이 없을 때의 오류를 처리합니다.
    3. JSON 문법이 깨졌을 때의 오류를 처리합니다.
"""

import json
from pathlib import Path


CURRENT_DIR = Path(__file__).parent


def read_json_safely(file_name: str) -> dict:
    """JSON 파일을 읽고 dict로 반환합니다.

    오류가 나면 프로그램을 바로 종료하지 않고 빈 dict를 반환합니다.
    """
    file_path = CURRENT_DIR / file_name
    try:
        text = file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError("파일이 없어요")
    # JSON 파일을 Dict로 변경
    return json.loads(text)



def main() -> None:
    # file1 = read_json_safely("config.json")
    # print(file1)
    # print(type(file1))
    # print(file1["app_name"])
    try:
        file = read_json_safely("config.json")
    except FileNotFoundError:
        print("파일이 없습니다")
        return
    print(file)


main()
