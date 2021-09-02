#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# 初始化美股股票数据库
# 股票列表：https://api.nasdaq.com/api/screener/stocks?tableonly=false&download=true
#
###############################################################################

import sqlite3 as sqlite

def init_ticker_list():
    con = sqlite.connect('/mnt/d/02Eugene/01Projects/trader_eugene/stock_db/stock_us.db')
    cur = con.cursor()
    # Create table
    cur.execute('''CREATE TABLE stocks(symbol text, name text, lastsale real, netchange real, pctchange real, marketCap real, country text, ipoyear real, volume real, sector text, industry text, url text)''')
    cur.commit()



if __name__ == '__main__':
    init_ticker_list()