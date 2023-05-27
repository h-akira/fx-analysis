#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-05-26 23:28:35

# Import
import sys
import os
import numpy
import time
import selenium
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\

""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-o", "--output", metavar="output-file", default="output", help="output file")
  parser.add_argument("-l", "--little", action="store_true", help="little endian")
  parser.add_argument("file", metavar="input-file", help="input file")
  options = parser.parse_args()
  return options

def main():
  # ArgumentParser
  options = parse_args()
  # CHROMEDRIVER = "/usr/bin/chromedriver"
  # driver_options = Options()
  # options.add_argument('--headless')
  # driver = webdriver.Chrome(CHROMEDRIVER, options=driver_options)
  # driver = webdriver.Chrome(options.file)
  # time.sleep(5)
  bs = BeautifulSoup(open(options.file,mode="r"), 'html.parser')
  # x = bs.find_all('td', attrs={"class":"td-render-commodity search-result-td"})
  # print(x[0].text)
  table = bs.find('table', attrs={"class":"search-result-table"})
  thead = table.find('thead')
  ths = thead.tr.find_all('th')
  columns_jp = []
  for th in ths:
    columns_jp.append(th.text)
  print(columns_jp)
  tbody = table.find('tbody')
  trs = tbody.find_all('tr')
  data = []
  for tr in trs:
    row = []
    for td in tr.find_all('td'):
      row.append(td.text)
    data.append(row)
  # columns_jp = [
  #     "通貨ペア",
  #     "注文タイプ",
  #     "取引種類  売買",
  #     "取引数量",
  #     "注文レート[執行条件]  現在値",
  #     "状態  失効理由",
  #     "約定レート",
  #     "約定日時  受渡日",
  #     "決済損益  取引手数料",
  #     "累計スワップ",
  #     "注文日時  有効期限",
  #     "注文番号",
  #     "変更  取消",
  #     ]
  # columns = [
  #     "pair",
  #     "type",
  #     "kind buy_sell",
  #     "quantity",
  #     "order_rate now_rate",
  #     "state revocation_reason",
  #     "contract_rate",
  #     "contract_datetime receipt_date",
  #     "profit commission",
  #     "swap",
  #     "order_datetime ecpiration_date",
  #     "number",
  #     "change delete",
  #     ]
  # print(data)
  df = pd.DataFrame(data=data,columns=columns_jp)
  df["pair"] = df["通貨ペア"]
  df["type"] = df["注文タイプ"]
  df["kind"] = df["\n取引種類\n\n売買\n"].str.split(expand=True)[0].str.strip()
  df["buy or sell"] = df["\n取引種類\n\n売買\n"].str.split(expand=True)[1].str.strip()
  df["quantity"] = df["取引数量"]
  df["order rate"] = df["注文レート[執行条件]現在値"].str.split("[",expand=True)[0]
  df["state and revocation reason"] = df["状態失効理由"]
  df["execution rate"] = df["約定レート "]
  df["execution date and time"] = df["約定日時受渡日"].str[:17]
  df["receipt date"] = df["約定日時受渡日"].str[17:].str.strip()
  df["profit"] = df["決済損益取引手数料"]
  df["swap"] = df["累計スワップ"]
  df["order date and time"] = df["注文日時有効期限"].str[:17]
  df["expiration date"] = df["注文日時有効期限"].str[17:].str.strip()
  df["order number"] = df["注文番号"]
  df["change and cancel"] = df["変更取消"]
  df = df.drop(columns=columns_jp)
  print(df)
  print(df["execution date and time"])




if __name__ == '__main__':
  main()
