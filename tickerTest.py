import pyupbit

# 코인 종류들을 가져오는 함수를 만들어 보자.


ticker_list = pyupbit.get_tickers(fiat="KRW")
print(ticker_list)

coin_list = []
for ticker in ticker_list:
    #print(ticker[4:10])
    coin_list.append(ticker[4:10]) #이렇게 하면 "KRW-ETH"에서 앞의 "KRW-" 4글자를 빼고부터 가져와진다. 즉, 뒤에 있는 코인 이름만 가져와진다.