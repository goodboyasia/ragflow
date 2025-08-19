import requests

url = "http://localhost:9083/chat/with/czzs"
headers = {
    "Authorization": "sdibdeyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJnb25nc2hhbmdsaWFuIiwiY3JlYXRlZCI6MTc1NTU2Nzc4NjA4NywidXNlcklkIjo1NjYzNjEzMTc1Njg1MTcsImV4cCI6MTc1NTg1MTc4Nn0.lNodMxSOnp7CYnTafn1KiTXYmsxQ4YFqDVACvGNhvro8BLkDlymsEROYHoyib-RYfAm0_g72vEiEBiLyLcEjLQ",
    "Content-Type": "application/json",
    "cache-control": "no-cache"
}
data = {
    "question": "如何登录系统",
    "stream": True,
    "session_id": "d6bec6f27cce11f09c24fa163e6699bf"
}

with requests.post(url, headers=headers, json=data, stream=True) as r:
    for line in r.iter_lines():
        if line:
            print("收到:", line.decode("utf-8"))
