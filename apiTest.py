# https://docs.upbit.com/reference/ticker%ED%98%84%EC%9E%AC%EA%B0%80-%EB%82%B4%EC%97%AD 여기서 가져온 코드다.

import requests

url = "https://api.upbit.com/v1/ticker"

param = {"markets": "KRW-BTC"}

response = requests.get(url, params=param)

upbitResult = response.json()

print(upbitResult[0]['trade_price'])  # 현재가
print(upbitResult[0]['acc_trade_volume_24h'])  # 24시간 거래량
print(upbitResult[0]['acc_trade_price_24h'])  # 24시간 누적 거래대금
print(upbitResult[0]['high_price'])  # 고가
print(upbitResult[0]['low_price'])  # 저가
print(upbitResult[0]['prev_closing_price'])  # 전일종가
print(upbitResult[0]['trade_volume'])  # 최근거래량
print(upbitResult[0]['signed_change_rate'])  # 부호가있는변화율
