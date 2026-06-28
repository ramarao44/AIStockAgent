# #import yfinance as yf

# symbol = "RELIANCE.NS"

# ticker = yf.Ticker(symbol)

# info = ticker.fast_info

# print("==========")
# print("Symbol:", symbol)
# print("Current Price:", info.get("lastPrice"))
# print("Day High:", info.get("dayHigh"))
# print("Day Low:", info.get("dayLow"))
# print("Volume:", info.get("lastVolume"))
# print("==========")

import yfinance as yf

ticker = yf.Ticker("RELIANCE.NS")

history = ticker.history(period="1mo")

print(history.head())