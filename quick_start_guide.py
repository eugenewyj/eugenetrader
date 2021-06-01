from __future__ import (absolute_import, division, print_function, unicode_literals)

import datetime
import os.path
import sys

import backtrader as bt
from backtrader.functions import If

class TestStrategy(bt.Strategy):
    params = (
        ('exitbars', 5),
        ('maperiod', 15),
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self) :
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open

        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.sma = bt.indicators.SMA(self.datas[0], period=self.params.maperiod)

    
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm: %.2f' % (order.executed.price, order.executed.value, order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm: %.2f' % (order.executed.price, order.executed.value, order.executed.comm))
            
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' % (trade.pnl, trade.pnlcomm))

    def next(self):
        self.log('Open, %.2f, Close, %.2f' % (self.dataopen[0], self.dataclose[0]))

        if self.order:
            return

        if not self.position:
            # if self.dataclose[0] < self.dataclose[-1]:
            #     if self.dataclose[-1] < self.dataclose[-2]:
            #         self.log('BUY CREATE %.2f' % self.dataclose[0])
            #         self.order = self.buy()
            if self.dataclose[0] > self.sma[0]:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()
        else:
            # if len(self) >= (self.bar_executed + self.params.exitbars):
            #      self.log('SELL CREATE, %.2f' % self.dataclose[0])
            #      self.order = self.sell()
            if self.dataclose[0] < self.sma[0]:
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()



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

    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    cerebro._broker.setcommission(0.001)

    print('Starting Protfolio Value: %.2f' % cerebro._broker.get_value())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro._broker.get_value())

    cerebro.plot()