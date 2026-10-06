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

from mypackage.file import read_json_safely


def main() -> None:
    # json을 dict로 변환함
    # file1 = read_json_safely("config.json")
    # print(file1)
    file2 = None
    try:
        file2 = read_json_safely("broken_config.json")
    except FileNotFoundError:  
        print("파일이 없습니다.")
        # 더이상 화면에 출력을 멈출려고 return을 사용함
        return 
    except json.decoder.JSONDecodeError as error:
        print("파일에 문제가 있습니다.")
    print(file2)


main()

