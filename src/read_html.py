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
  parser.add_argument("-c", "--csv", metavar="csv-file", default="data.csv", help="csv file to save DataFrame")
  # parser.add_argument("-o", "--output", metavar="output-file", default="output.csv", help="output file")
  # parser.add_argument("-l", "--little", action="store_true", help="little endian")
  parser.add_argument("file", metavar="html-file", help="input file")
  options = parser.parse_args()
  return options

def main():
  # ArgumentParser
  options = parse_args()
  if os.path.isfile(options.csv):
    main_df = pd.read_csv(options.csv, header=0, dtype="object", na_values="")
    before_row = main_df.shape[0]
    # print(main_df)
  else:
    main_df=pd.DataFrame()
    before_row = 0
  print(main_df.dtypes)
  # print(main_df)
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
  # print(columns_jp)
  tbody = table.find('tbody')
  trs = tbody.find_all('tr')
  data = []
  for tr in trs:
    row = []
    for td in tr.find_all('td'):
      row.append(td.text)
    data.append(row)
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
  df["profit"] = df["決済損益取引手数料"].str.replace(",","")
  df["swap"] = df["累計スワップ"]
  df["order date and time"] = df["注文日時有効期限"].str[:17]
  df["expiration date"] = df["注文日時有効期限"].str[17:].str.strip()
  df["order number"] = df["注文番号"]
  df["change and cancel"] = df["変更取消"]
  df = df.drop(columns=columns_jp)
  
  print("main_df")
  print(main_df)
  main_df = pd.concat([main_df, df])
  print("連結")
  print(main_df)
  # main_df = main_df.drop_duplicates(subset=["order number"]).sort_values(by="order number", ascending=True)
  main_df = main_df.drop_duplicates(subset=["order number"])
  print("削除")
  print(main_df)
  main_df = main_df.sort_values(by="order number", ascending=True)
  print("並べ替え")
  print(main_df)
  df.to_csv(options.csv, header=True, index=False)
  # print(df.sort_values(by="order number", ascending=True))
  print(f"{df.shape[0]-before_row}行追加しました．")

if __name__ == '__main__':
  main()
