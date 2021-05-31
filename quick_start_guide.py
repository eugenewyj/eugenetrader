from __future__ import (absolute_import, division, print_function, unicode_literals)

import backtrader as bt
from backtrader import cerebro

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    print('Starting Protfolio Value: %.2f' % cerebro._broker.get_value())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro._broker.get_value())