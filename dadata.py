import dadata

token = "43d65be73cd09ab211517def88a1f3770698a41b"
secret = "5053169ec71b450e3b3133237055356dbc7df94d"   
dadataa = dadata.D(token, secret)
result = dadataa.suggest("okpd2", input())
dadataa.close()
print(result)