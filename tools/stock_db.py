#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# 初始化美股股票数据库
# 股票列表：https://api.nasdaq.com/api/screener/stocks?tableonly=false&download=true
#
###############################################################################
import logging
import sqlite3 as sqlite

logging.basicConfig(
    format='%(levelname)s: %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

con = sqlite.connect('../stock_db/stock_us.db')

def maintain_db_schema():
    '''维护数据库结构
    维护美股股票相关数据库表结构及初始化相关数据
    '''
    cur = con.cursor()
    create_stock_list = '''
    CREATE TABLE IF NOT EXISTS stock_list(
        symbol      TEXT PRIMARY KEY NOT NULL,
        name        TEXT NOT NULL,
        last_sale   REAL,
        net_change  REAL,
        pct_change  REAL,
        market_cap  REAL,
        country     TEXT,
        ipo_year    INT,
        volume      REAL,
        sector      TEXT,
        industry    TEXT,
        url         TEXT
    )
    '''
    cur.execute(create_stock_list)
    con.commit()
    logger.info("维护数据库表[stock_list]")


if __name__ == '__main__':
    maintain_db_schema()