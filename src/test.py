#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-05-23 02:02:40

# Import
import sys
import os
import pandas as pd
import mplfinance as mpf
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
  print(df)
  mpf.plot(df.head(100), type="candle", mav=[20], hlines={'hlines':[136.28,136.32],'colors':['g','r']},
      vlines={'vlines':['2023-05-01 07:23','2023-05-01 07:43'],'colors':['g','r']})

if __name__ == '__main__':
  main()
