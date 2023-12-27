# 小市值轮动策略

## 前言

本节将实践小市值轮动策略，包括：

- 策略的详细思路

- 策略的回测效果

- 策略的优化思路

- 优化后的效果

## 基本策略思路

1. 每天选出市值最小的 `stocksTotalNum` 只股票，作为候选股票
```python
    scu = get_all_securities(date=context.current_dt).index.tolist()
    # 选出市值排名最小的前 stocksTotalNum 只股票
    q = query(valuation.code)\
        .filter(valuation.code.in_(scu))\
        .order_by(valuation.market_cap.asc())\
        .limit(g.stocksTotalNum)
    df = get_fundamentals(q)
    
    buylist = list(df['code'])
```

2. 判断以购入股票中是否存在不在候选股票中的股票，如果存在，则全部卖出，此时剩余买入股票数为 `stocksHasNum`
```python
    stocksHasNum = 0
    for stock in context.portfolio.positions:
        if stock not in buylist:
            order_target(stock, 0)
        else:
            stocksHasNum += 1
```

3. 判断候选股票中是否存在没有买入，若存在，则使用可用资金的 `1/(stocksTotalNum-stocksHasNum)` 买入

```python
    wouldBuyNum = (g.stocksTotalNum - stocksHasNum)
    position_per_stk = context.portfolio.cash / wouldBuyNum if wouldBuyNum > 0 else 0
    for stock in buylist:
        if stock not in context.portfolio.positions:
            order_value(stock, position_per_stk)
```

## 策略的回测效果

在 2023-01-01 - 2023-12-26 上进行了回测，效果惨淡，-80% 左右的战绩