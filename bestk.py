import pyupbit
import numpy as np

def Get_bestk():
    bestk_result = 0
    bestk_k = 0
    def get_ror(k):
        df = pyupbit.get_ohlcv("KRW-BTC", count=7)
        df['range'] = ((df['high'] - df['low'])/3) * k
        df['target'] = df['open'] + df['range'].shift(1)

        df['ror'] = np.where(df['high'] > df['target'],
                            df['close'] / df['target'],
                            1)

        ror = df['ror'].cumprod()[-2]
        return ror


    for k in np.arange(0.1, 1.0, 0.1):
        ror = get_ror(k)
        if ror > bestk_result:
            bestk_k = k
            bestk_result = ror
        # print("%.1f %f" % (k, ror))

    return bestk_k

print(Get_bestk())