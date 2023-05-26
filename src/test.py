#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-05-23 02:02:40

# Import
import sys
import os
import pandas as pd
import mplfinance as mpf
import datetime
import talib
import numpy
# import matplotlib.pyplot as plt

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\

""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  # parser.add_argument("-o", "--output", metavar="output-file", default="output", help="output file")
  # parser.add_argument("-l", "--little", action="store_true", help="little endian")
  parser.add_argument("file", metavar="input-file", help="input file")
  options = parser.parse_args()
  return options

def main():
  options = parse_args()
  df = pd.read_csv(options.file, encoding='shift_jis').rename(columns={'日時':'date', '始値(BID)':'Open', '高値(BID)':'High', '安値(BID)':'Low', '終値(BID)':'Close'})
  df["date"] = pd.to_datetime(df["date"])
  df.set_index("date", inplace=True)
  df = df.head(100)
  print(df)
  dates_df = pd.DataFrame(df.index)
  buy_time=pd.Timestamp('2023-05-01 07:23'),
  sell_time=pd.Timestamp('2023-05-01 07:33')
  y1value = df['Close'].max()
  y2value = df['Low'].min()
  where_values = pd.notnull(dates_df[(dates_df>=buy_time)&(dates_df<=sell_time)])['date'].values
  print(where_values)
  period = 20  # 任意の値を設定
  sigma = 2  # 任意の値を設定
  # 下記は移動平均の種類
  # 0:単純移動平均
  moving_average_type = 0
  bb_up, bb_middle, bb_down = talib.BBANDS(numpy.array(df['Close']),
    period, sigma, sigma, moving_average_type)
  df['bb_up']=bb_up
  # print(df)
  # mpf.plot(df, type="candle", mav=[20], hlines={'hlines':[136.28,136.32],'colors':['g','r']},
  df['bb_middle']=bb_middle
  df['bb_down']=bb_down
  apd = mpf.make_addplot(df[['bb_up', 'bb_middle', 'bb_down']],linestyle='dashdot',alpha=0.5)
  print(df)
  # print(bb_up.__class__)
  # 移動平均線の場合は下記に引数`mav[20]`など
  mpf.plot(df, type="candle", addplot=apd, hlines={'hlines':[136.28,136.32],'colors':['g','r']},
      fill_between=dict(y1=y1value, y2=y2value, where=where_values, alpha=0.2), style="yahoo")
      # vlines={'vlines':['2023-05-01 07:23','2023-05-01 07:43'],'colors':['g','r']},
      # fill_between=dict(
      # x1=pd.Timestamp('2023-05-01 07:23'),
      # x2=pd.Timestamp('2023-05-01 07:23')
      # x1=10,
      # x2=20)
      # x1=datetime.datetime.strptime('2023-05-01 07:23','%Y-%m-%d %H:%M'),
      # x2=datetime.datetime.strptime('2023-05-01 07:23','%Y-%m-%d %H:%M')
  # fill_between=dict(x1='2023-05-01 07:23',x2='2023-05-01 07:43'))
               #x1='2023-05-01 07:23',x2='2023-05-01 07:43'))

if __name__ == '__main__':
  main()
