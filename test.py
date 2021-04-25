import pyupbit

access = "Ku9OvXuFqVnqqMPKxaylZutfdc7ALBxs8deIvyfR"          # 본인 값으로 변경
secret = "mSrhY0uxlYOxp4QP8507X19ZWkQnvpyDNWTx4NGH"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

# print(upbit.get_balance("KRW-XRP"))     # KRW-XRP 조회
#print(upbit.get_balance("KRW")) # 보유 현금 조회
money = str(upbit.get_balance("KRW"))
print(money + "원")
#보유 현금