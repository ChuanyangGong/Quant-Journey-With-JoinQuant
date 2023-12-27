# 导入函数库
from jqdata import *

def initialize(context):
    run_daily(period, time='every_bar')
    g.stocksTotalNum = 10  # 买入
    
def period(context):
    # 获取当天的股票列表
    scu = get_all_securities(date=context.current_dt).index.tolist()
    # 选出市值排名最小的前 stocksTotalNum 只股票
    q = query(valuation.code)\
        .filter(valuation.code.in_(scu))\
        .order_by(valuation.market_cap.asc())\
        .limit(g.stocksTotalNum)
    df = get_fundamentals(q)
    
    buylist = list(df['code'])
    
    # 卖出不在最便宜的 10 只股票的股票
    stocksHasNum = 0
    for stock in context.portfolio.positions:
        if stock not in buylist:
            order_target(stock, 0)
        else:
            stocksHasNum += 1
    
    # 买入还没买的
    wouldBuyNum = (g.stocksTotalNum - stocksHasNum)
    position_per_stk = context.portfolio.cash / wouldBuyNum if wouldBuyNum > 0 else 0
    for stock in buylist:
        if stock not in context.portfolio.positions:
            order_value(stock, position_per_stk)