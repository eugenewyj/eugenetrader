from __future__ import (absolute_import, division, print_function, unicode_literals)

import datetime
import os.path
import sys

import backtrader as bt

class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self) :
        self.dataclose = self.datas[0].close

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])



if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    cerebro.addstrategy(TestStrategy)

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    print(modpath)
    datapath = os.path.join(modpath, '../backtrader/datas/orcl-1995-2014.txt')
    print(datapath)
    # datapath = os.path.realpath(datapath)
    # print(datapath)

    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2000, 1, 1),
        todate=datetime.datetime(2000, 12, 31),
        reversed=False
    )

    cerebro.adddata(data)

    cerebro._broker.set_cash(100000.00)

    print('Starting Protfolio Value: %.2f' % cerebro._broker.get_value())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro._broker.get_value())