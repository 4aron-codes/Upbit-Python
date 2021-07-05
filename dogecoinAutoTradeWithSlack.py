from getTickers import KRW_tickers_list
import time
import pyupbit
import datetime
import requests

access = ""
secret = ""
myToken = ""
tickers = pyupbit.get_tickers()

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_balance(coin):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == coin:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
# 시작 메세지 슬랙 전송
post_message(myToken,"#stock", "autotrade start")

def get_KRW_tickers():
    KRW_tickers_list = []
    for i in tickers:
        if i[0:3] == 'KRW':
            KRW_tickers_list.append(i)
    return KRW_tickers_list

while True:
    while True:
        KRW_tickers_list = get_KRW_tickers()
        for ticker_name in KRW_tickers_list:
            try:
                now = datetime.datetime.now()
                start_time = get_start_time(ticker_name)
                end_time = start_time + datetime.timedelta(days=1)

                if start_time < now < end_time - datetime.timedelta(seconds=10):
                    target_price = get_target_price(ticker_name, 0.7)
                    ma15 = get_ma15(ticker_name)
                    current_price = get_current_price(ticker_name)
                    if target_price < current_price and ma15 < current_price:
                        krw = get_balance("KRW")
                        if krw > 100:
                            buy_result = upbit.buy_market_order(ticker_name, krw*0.9995)
                            post_message(myToken,"#stock", ticker_name+" buy : " +str(buy_result))
                else:
                    doge = get_balance(ticker_name[4:])
                    if doge > 10:
                        sell_result = upbit.sell_market_order(ticker_name, doge*0.9995)
                        post_message(myToken,"#stock", ticker_name[4:]+" sell : " +str(sell_result))
                time.sleep(0.1)
            except Exception as e:
                print(e)
                post_message(myToken,"#stock", e)
                time.sleep(1)
