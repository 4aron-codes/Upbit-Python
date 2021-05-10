import pyupbit

access = "I2UxPw29ixxiw4yKUguS4dtcfvBYPnkIKi1Tmw7D"          # 본인 값으로 변경
secret = "F8RNFqykSjT0JruTDXIFw5LTHGsOf2s47tdHzNaA"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-DOGE"))     # KRW-XRP 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회