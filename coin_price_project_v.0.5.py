import sys
import time  # 왜 from datetime import time으로 했을 때 에러가 났을까?

import pyupbit
import requests as requests
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

form_class = uic.loadUiType("ui/coinPriceUi.ui")[0]


class CoinViewThread(QThread): # 이걸 스레드로 해야 컴퓨터가 멀티태스킹(비슷한 거) 가능
    # 시그널 함수 정의 ㅋ
    coinDataSent = pyqtSignal(float, float, float, float, float, float, float, float)

    def __init__(self, ticker):  # MainWindow에서 thread 클래스에 인수를 전달하려면? 이렇게 초기화자의 매개변수로 추가하면 된다.
        super().__init__()  # CoinViewThread는 티커를 바꿀 수 있는 권한이 없다. 애초부터 직접 ui에 접근하지도 않잖아. MainWindow에서 ticker를 갖고 와야 한다.
        self.ticker = ticker
        self.alive = True

    def run(self):
        # 업비트 정보 호출

        while self.alive:
            url = "https://api.upbit.com/v1/ticker"

            param = {
                "markets": f"KRW-{self.ticker}"}  # 받아 온 ticker 값을 파라미터 값으로 설정. (왜 f string 쓰냐? markets는 원래 "KRW-BTC" 이런 형태였으니까.)

            response = requests.get(url, params=param)

            upbitResult = response.json()

            trade_price = upbitResult[0]['trade_price']  # 현재가
            acc_trade_volume_24h = upbitResult[0]['acc_trade_volume_24h']  # 24시간 거래량
            acc_trade_price_24h = upbitResult[0]['acc_trade_price_24h']  # 24시간 누적 거래대금
            high_price = upbitResult[0]['high_price']  # 고가
            low_price = upbitResult[0]['low_price']  # 저가
            prev_closing_price = upbitResult[0]['prev_closing_price']  # 전일종가
            trade_volume = upbitResult[0]['trade_volume']  # 최근거래량
            signed_change_rate = upbitResult[0]['signed_change_rate']  # 부호가있는변화율

            # Signal emit! 그 순간? 슬롯에 이 8개의 코인 정보 변수를 실어보내요
            self.coinDataSent.emit(float(trade_price),
                                   float(acc_trade_volume_24h),
                                   float(acc_trade_price_24h),
                                   float(high_price),
                                   float(low_price),
                                   float(prev_closing_price),
                                   float(trade_volume),
                                   float(signed_change_rate)  # 옆으로 쭉 써도 된다. 그냥 가독성을 위해서 내렸을 뿐.
                                   )

            time.sleep(1)  # 디도스 공격으로 간주되지 않게 api 호출에 딜레이를 걸자. (indentation 틀리지 마셈 ㅋ while문을 1초 1반복으로 만들어야 ㅋ)

    def close(self):  # 프로그램 꺼 줄 용도로 만든 함수
        self.alive = False


class MainWindow(QMainWindow, form_class):
    def __init__(self, ticker='BTC'):  # 맨 처음 시작할 때 티커는 BTC로 하자.
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("BitCoin Price Overview")
        self.setWindowIcon(QIcon("icons/bitcoin.png"))
        self.statusBar().showMessage('ver 1.0')
        self.ticker = ticker

        self.cvt = CoinViewThread(ticker)  # 코인정보 가져오는 스레드 클래스를 멤버 객체로 선언
        self.cvt.coinDataSent.connect(self.fillCoinData)  # 스레드 시그널에서 온 데이터를 받아 줄 슬롯 함수를 연결
        self.cvt.start()  # 스레드 클래스의 run()함수를 호출. (함수 시작)
        self.comboBox_setting()  # 콤보박스 초기화하는 함수 호출.

    def comboBox_setting(self):  # 코인 목록 콤보박스 세팅
        ticker_list = pyupbit.get_tickers(fiat="KRW")  # 업비트에 존재하는 코인 티커들 다 불러모아. (네 식구들 다 불러모아.)

        coin_list = []
        for ticker in ticker_list:
            coin_list.append(ticker[4:10])  # ticker들에서 앞의 'KRW-' 자르고 coin_list에 추가.

        # coin_list = ['BTC', 'ETH', 'AVAX'] 업비트의 모든 코인을 다 불러올 필요가 없다면 이런 식으로 관심있는 애들만 몇 개 추가해도 됨.

        coin_list1 = ['BTC']  # 너희는 알트코인도 아닌데 가오가 있지. 상단에 나와야 해.
        coin_list2 = ['ETH']

        coin_list.remove('BTC')  # 상단에 BTC랑 ETH 있는데 하단에도 또 있으면 중복이니까 이상하니까...
        coin_list.remove('ETH')

        coin_list3 = sorted(coin_list)

        coin_list4 = coin_list1 + coin_list2 + coin_list3

        self.coin_comboBox.addItems(coin_list4)  # 코인 목록을 콤보박스에 추가
        self.coin_comboBox.currentIndexChanged.connect(
            self.coin_select_ComboBox)  # 콤보박스의 값이 변경되었을 때 (다른 코인을 선택했을 때) 연결된 함수 실행

    def coin_select_ComboBox(self):
        coin_ticker = self.coin_comboBox.currentText()  # 콤보박스에서 유저가 선택한 ticker 불러오기
        self.ticker = coin_ticker
        self.coin_ticker_label.setText(self.ticker) # 콤보박스에서 선택된 ticker로 ui상의 레이블 세팅. self.ticker 쓰나 coin_ticker 쓰나 그게그거.

        self.cvt.close()  # 어. 현재 스레드 개체 정지시켜. (while문 종료) 현재 실행되고 있는 스레드를 껐다 켜야 새로 선택한 ticker를 활용한 코인 정보가 제대로 불러와진다.

        self.cvt = CoinViewThread(self.ticker)  # 그럼 스레드를 껐다 켜는 건 어케 하나? '껐다 새롭게 생성해야' 한다.
        self.cvt.coinDataSent.connect(self.fillCoinData)
        self.cvt.start()


    # 스레드 클래스에서 보내 준 데이터를 받아 주는 슬롯 함수.
    def fillCoinData(self, trade_price, acc_trade_volume_24h, acc_trade_price_24h,
                     high_price, low_price, prev_closing_price, trade_volume, signed_change_rate):

        self.coin_price_label.setText(f"{trade_price:,.0f}원")  # 코인 현재 가격
        self.coin_changerate_label.setText(f"{signed_change_rate:+.2f}%")  # 가격변화율
        self.acc_trade_volume_label.setText(f"{acc_trade_volume_24h:.4f} {self.ticker}")  # 24시간 거래량 (단위: 해당 코인)
        self.acc_trade_price_label.setText(f"{acc_trade_price_24h:,.0f}원")  # 24시간 거래금액 (단위: 원)
        self.trade_volume_label.setText(f"{trade_volume:.6f} {self.ticker}")  # 최근거래량
        self.high_price_label.setText(f"{high_price:,.0f}원")  # 당일 고가
        self.low_price_label.setText(f"{low_price:,.0f}원")  # 당일 저가
        self.prev_closing_price_label.setText(f"{prev_closing_price:,.0f}원")  # 전일 종가
        self.__updateStyle()

    def __updateStyle(self):  # __로 함수 이름이 시작하는 이유? 그냥 자의적이다.
        # 프로그래머들이 "부가 기능을 담당하는 함수는 __로 시작하게 이름 짓자"라고 약속해서. init(self)이 __init(self)__인 거랑 비슷한 이유다, ㅋ

        if '-' in self.coin_changerate_label.text():  # 레이블에 방금 찍었던 값을 가져와서 조건으로 쓰기~~ 이런 식으로 흔하게 조건 만든다. (변화율만 따로 가져오는 시그널 - 슬롯 또 만드는 건 귀찮으니까.)
            self.coin_changerate_label.setStyleSheet("background-color:RoyalBlue; color:white;")
            self.coin_price_label.setStyleSheet("color:RoyalBlue;")

        else:
            self.coin_changerate_label.setStyleSheet("background-color:Crimson; color:white;")
            self.coin_price_label.setStyleSheet("color:Crimson;")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
