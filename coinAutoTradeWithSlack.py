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
    """KRW 종목 수집"""
    KRW_tickers_list = []
    for i in tickers:
        if i[0:3] == 'KRW':
            KRW_tickers_list.append(i)
    return KRW_tickers_list

def get_remained_time(ticker_name):
    """9, 15, 21, 3시 중 가장 가까운 남은시간 계산"""
    now = datetime.datetime.now()
    start_time = get_start_time(ticker_name)
    end_time = start_time + datetime.timedelta(days=1)

    remained_time_list = []
    remained_Time0 = (end_time - datetime.timedelta(seconds=10) - now)
    remained_Time0 = remained_Time0
    if remained_Time0.days == 0:
        remained_time_list.append(remained_Time0)

    remained_Time1 = (end_time - datetime.timedelta(hours=6, seconds=10) - now)
    remained_Time1 = remained_Time1
    if remained_Time1.days == 0:
        remained_time_list.append(remained_Time1)

    remained_Time2 = (end_time - datetime.timedelta(hours=12, seconds=10) - now)
    remained_Time2 = remained_Time2
    if remained_Time2.days == 0:
        remained_time_list.append(remained_Time2)

    remained_Time3 = (end_time - datetime.timedelta(hours=18, seconds=10) - now)
    remained_Time3 = remained_Time3
    if remained_Time3.days == 0:
        remained_time_list.append(remained_Time3)
    
    return min(remained_time_list)

while True:
    while True:
        KRW_tickers_list = get_KRW_tickers()
        for ticker_name in KRW_tickers_list:
            print(ticker_name)
            try:
                now = datetime.datetime.now()
                start_time = get_start_time(ticker_name)
                end_time = start_time + datetime.timedelta(days=1)
                time0 = end_time < now < end_time - datetime.timedelta(seconds=10)
                time1 = start_time + datetime.timedelta(hours=6) < now < end_time - datetime.timedelta(hours=18, seconds=10)
                time2 = start_time + datetime.timedelta(hours=12) < now < end_time - datetime.timedelta(hours=12, seconds=10)
                time3 = start_time + datetime.timedelta(hours=18) < now < end_time - datetime.timedelta(hours=6, seconds=10)

                if not time0 and not time1 and not time2 and not time3:
                    target_price = get_target_price(ticker_name, 0.5)
                    ma15 = get_ma15(ticker_name)
                    current_price = get_current_price(ticker_name)
                    if target_price < current_price and ma15 < current_price:
                        print(ticker_name)
                        krw = get_balance("KRW")
                        if krw > 100:
                            buy_result = upbit.buy_market_order(ticker_name, krw*0.9995)
                            post_message(myToken,"#stock", ticker_name+" buy : " +str(buy_result))
                            while (not time0 and not time1 and not time2 and not time3):
                                time.sleep(1)
                            stock_balance = get_balance(ticker_name[4:])
                            if stock_balance > get_current_price(ticker_name[4:])/5000:
                                sell_result = upbit.sell_market_order(ticker_name, stock_balance*0.9995)
                                post_message(myToken,"#stock", ticker_name[4:]+" sell : " +str(sell_result))
                    
                #time.sleep(0.1)
            except Exception as e:
                print(e)
                post_message(myToken,"#stock", ticker_name)
                post_message(myToken,"#stock", e)
                time.sleep(1)
