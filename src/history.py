#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-05-26 23:28:35

# Import
import sys
import os
import numpy
import time
# import selenium
import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup






class Trade:
  def __init__(self, new=None, settlement=None):
    self.new = new
    self.settlement = settlement
  def search_new(self, df, sell)
    pass
    


def GMO_read_csv(file_name, exception=False):
  if os.path.isfile(file_name):
    df = pd.read_csv(file_name, header=0, dtype="object", na_values="")
    df["profit"] = df["profit"].str.replace(",","").astype(int)
    df["swap"] = df["swap"].str.replace(",","").astype(int)

  else:
    if exception:
      raise Exception
  return df

def GMO_html2df(html):
  bs = BeautifulSoup(html, 'html.parser')
  table = bs.find('table', attrs={"class":"search-result-table"})
  thead = table.find('thead')
  ths = thead.tr.find_all('th')
  columns_jp = []
  for th in ths:
    columns_jp.append(th.text)
  tbody = table.find('tbody')
  trs = tbody.find_all('tr')
  data = []
  for tr in trs:
    row = []
    for td in tr.find_all('td'):
      row.append(td.text)
    data.append(row)
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
  df["profit"] = df["決済損益取引手数料"].str.replace(",","").astype(int)
  df["swap"] = df["累計スワップ"].str.replace(",","").astype(int)
  df["order date and time"] = df["注文日時有効期限"].str[:17]
  df["expiration date"] = df["注文日時有効期限"].str[17:].str.strip()
  df["order number"] = df["注文番号"]
  df["change and cancel"] = df["変更取消"]
  df = df.drop(columns=columns_jp)
  return df

def add_data(*args):
  df = pd.concat(args)
  df = df.drop_duplicates(subset=["order number"])
  df = df.sort_values(by="order number", ascending=True)
  return df

def save_df(df, file_name):
  df.to_csv(file_name, header=True, index=False)

def test():
  import argparse
  parser = argparse.ArgumentParser(description="test")
  parser.add_argument("-c", "--csv", metavar="csv-file")
  parser.add_argument("html", metavar="html-file")
  options = parser.parse_args()
  df = GMO_read_csv(options.csv)
  add_df = GMO_html2df(open(options.html, mode="r").read())
  df = add_data(df, add_df)
  print(df)
  save_df(df,options.csv)

if __name__ == '__main__':
  test()
