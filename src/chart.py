#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-05-23 02:02:40

# Import
import pandas as pd
import mplfinance as mpf
import talib
import numpy
  
def GMO2DataFrame(file_name):
  # GMOクリック証券からダウンロードしたヒストリカルデータ（CSVファイル）を読み込み，
  # mplfinanceで扱えるデータフレームにして返す．
  df = pd.read_csv(file_name, encoding='shift_jis').rename(
    columns={
      '日時':'date', 
      '始値(BID)':'Open', 
      '高値(BID)':'High', 
      '安値(BID)':'Low', 
      '終値(BID)':'Close'
    }
  )
  df["date"] = pd.to_datetime(df["date"])
  df.set_index("date", inplace=True)
  return df

def add_BBands(df,period=20,nbdev=2,matype=0):
  # mplfinanceのデータフレームにボリンジャーバンドの列を追加する．
  bb_up, bb_middle, bb_down = talib.BBANDS(numpy.array(df['Close']), timeperiod=period, nbdevup=nbdev, nbdevdn=nbdev, matype=matype)
  df['bb_up']=bb_up
  df['bb_middle']=bb_middle
  df['bb_down']=bb_down
  return df

def gen_chart(df,buy_time=None,sell_time=None,hlines=None,vlines=None,style="yahoo"):
  # hlinesとvlinseは辞書型
  # 例: {'hlines':[136.28,136.32],'colors':['g','r']}
  plot_args = {
    "type":"candle"
  }
  if buy_time != None and sell_time != None:
    if buy_time.__class__ == str:
      buy_time=pd.Timestamp(buy_time),
    if sell_time.__class__ == str:
      sell_time=pd.Timestamp(sell_time),
    dates_df = pd.DataFrame(df.index)
    y1value = df['Close'].max()
    y2value = df['Low'].min()
    where_values = pd.notnull(dates_df[(dates_df>=buy_time)&(dates_df<=sell_time)])['date'].values
    plot_args["fill_between"] = dict(y1=y1value, y2=y2value, where=where_values, alpha=0.2) 
  if "bb_up" in df.columns and "bb_middle" in df.columns and "bb_down" in df.columns:
    plot_args["addplot"] = mpf.make_addplot(df[['bb_up', 'bb_middle', 'bb_down']],linestyle='dashdot',alpha=0.5)
  if hlines != None:
    plot_args["hlines"] = hlines
  if vlines != None:
    plot_args["vlines"] = vlines
  mpf.plot(df, **plot_args)

