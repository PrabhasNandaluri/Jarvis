import yfinance as yf
import os
import csv
import json

with open("Data/Input_Constants.Json", "r") as file:
  constants = json.load(file)

class Data:
  def __init__(self) -> None:
    pass

class Telegram_Bot:
  def __init__(self) -> None:
    pass

files : list = []

def download_data(symbol : str | list) -> None:
  try:
    files = os.listdir(os.getcwd() + "\Data\stocks_data")
  except FileNotFoundError:
    os.makedirs("Data\stocks_data")
  
  filename = symbol + '.csv'
  
  if filename not in files:
    data = yf.download(symbol + '.ns')
    data.to_csv(f'{os.getcwd()}\Data\stocks_data\{filename}')
  else:
    print("file Exist")

def Nifty50_list() -> list:
  nifty50_stocks : list = []
  with open("data\data.csv", "r") as nifty50:
    csv_reader = csv.reader(nifty50)
    for line in csv_reader:
      print(line[0])
      nifty50_stocks.append(line[0])
  return nifty50_stocks

def delivery_data():
  pass

def main():
  symbol = Nifty50_list()
  for stock in symbol:
    data = yf.download(stock + ".ns")
    data.to_csv(f'{os.getcwd()}\Data\stocks_data\{stock}.csv')

if __name__ ==  "__main__":
  main()