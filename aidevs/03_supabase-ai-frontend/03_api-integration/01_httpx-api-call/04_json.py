# https://jsonplaceholder.typicode.com/
# posts 정보를 가지고 와서 출력 한다.
# 출력할때: user_id,title,body를 출력한다.

import httpx

API_URL = "https://jsonplaceholder.typicode.com/posts"

response = httpx.get(API_URL, timeout=5.0)

if response.status_code == 200:
    result=response.json()
    for data in result:
        print(f"{data["userId"]} {data["body"]} {data["title"]}")

