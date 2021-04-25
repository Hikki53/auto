import requests
import pandas as pd
import time
import webbrowser
import pyupbit


access = "z5M4ONToj7GhqAxnt6xS0S89dO7lbAXZ6SdW0TOi"
secret = "ZKWvX5MOvftW405reyGw6MJtxhh1l9xTafjd0qxv"

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

chk = 0

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0


while True:
    url = "https://api.upbit.com/v1/candles/minutes/1"

    querystring = {"market":"KRW-DOGE","count":"500"}

    response = requests.request("GET", url, params=querystring)

    data = response.json()

    df = pd.DataFrame(data)

    df=df.reindex(index=df.index[::-1]).reset_index()

    df['close']=df["trade_price"]


    def rsi(ohlc: pd.DataFrame, period: int = 14):
        ohlc["close"] = ohlc["close"]
        delta = ohlc["close"].diff()

        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0

        _gain = up.ewm(com=(period - 1), min_periods=period).mean()
        _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()

        RS = _gain / _loss
        return pd.Series(100 - (100 / (1 + RS)), name="RSI")

    rsi = rsi(df, 14).iloc[-1]

    print('Upbit 10 minute BTC RSI:', rsi)

    try:
        krw = get_balance("KRW")
        if krw > 5000 and chk == 0 and rsi <35 :
            upbit.buy_market_order("KRW-DOGE", krw*0.9995)
            chk = 1
            doge = get_balance("DOGE")
        if rsi >= 60 and chk == 1:
            upbit.sell_market_order("KRW-DOGE", doge*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)

    

    time.sleep(1)

