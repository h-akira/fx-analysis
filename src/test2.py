#!/usr/bin/env python3

# Import
import pandas as pd
import mplfinance as mpf
import talib
import numpy
import chart

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
  df = chart.GMO_csv2DataFrame(options.file)
  df = chart.add_BBands(df,20,2,0)
  # chart.gen_chart(df.head(100),"2023-05-01 07:23","2023-05-01 07:33",dict(hlines=[136.28,136.32],colors=["g","r"]),figsize=(10,5),savefig=dict(fname="test.png",dpi=1000))
  chart.gen_chart(df.head(100),"2023-05-01 07:23","2023-05-01 07:33",dict(hlines=[136.28,136.32],colors=["g","g"],linewidths=[0.1,0.1]))

if __name__ == '__main__':
  main()
