#!/usr/bin/env python3
"""纯做市模拟器（hummingbot 核心概念的原生实现，M0）

上游 Hummingbot（21.2k★，Apache-2.0）是做市/高频交易机器人框架（重型应用，
通常 Docker 部署）。本插件 v0 **原生实现其核心概念**——pure market making：
围绕中间价挂双边价差单，按库存偏移报价，定期刷新；实盘路由由家族
fail-closed 护栏锁死（M2 才接 hummingbot docker 作为执行器）。

模拟假设（如实标注，M1 升级）：
- 1m K 线"触及即成交"（bar low<=bid 即买单成交，high>=ask 即卖单成交），
  非订单簿排队撮合——真实做市的逆向选择/排队损耗被低估；
- 每根 bar 至多成交一侧。

用法：
  python3 scripts/mm_sim.py --data /tmp/btc_1m.json \
      --params '{"bid_spread_bps":10,"ask_spread_bps":10,"order_btc":0.01,"inventory_skew":0.5,"fee_bps":2}'
"""
import argparse, datetime as dt, json, os, sys


def simulate(bars, bid_bps, ask_bps, order_amt, inv_skew, fee_bps, base_inv, quote_cash):
    """bars: [[date, open, close, high, low, volume], ...]（1m）"""
    fee = fee_bps / 10000
    inventory, cash, fills_buy, fills_sell = base_inv, quote_cash, 0, 0
    curve, quotes_log = [], []
    refresh = max(1, int(os.environ.get("MM_REFRESH_BARS", "1")))
    open_bid = open_ask = None
    for i, (d0, o, c, h, l, v) in enumerate(bars):
        if i % refresh == 0:
            mid = o
            # 库存偏移（正确方向）：多头库存越重，双边报价越低（买单更难成交、
            # 卖单更易成交→库存回归）；空头反之。偏移设上限防病态报价。
            span = (bid_bps + ask_bps) / 2
            raw = inv_skew * (inventory / order_amt) * span
            skew = max(-span, min(span, raw)) / 10000
            # 库存断路器：|库存| 超过 5 倍单量时只挂去库存一侧（hummingbot 同款思想）
            quote_bid = abs(inventory) < 5 * order_amt or inventory > 0
            quote_ask = abs(inventory) < 5 * order_amt or inventory < 0
            open_bid = mid * (1 - bid_bps / 10000 - skew) if quote_bid else None
            open_ask = mid * (1 + ask_bps / 10000 - skew) if quote_ask else None
        filled = []
        if open_bid is not None and l <= open_bid:
            inventory += order_amt; cash -= open_bid * order_amt * (1 + fee)
            fills_buy += 1; filled.append("bid")
        if open_ask is not None and h >= open_ask:
            inventory -= order_amt; cash += open_ask * order_amt * (1 - fee)
            fills_sell += 1; filled.append("ask")
        if filled:
            quotes_log.append({"bar": d0, "mid": round(o, 2), "bid": round(open_bid, 2),
                               "ask": round(open_ask, 2), "filled": filled,
                               "inv": round(inventory, 4)})
        curve.append(cash + inventory * c)
    last = bars[-1][2]
    final = cash + inventory * last
    start_mid = bars[0][1]
    return {
        "engine": "pure-market-making v0 (1m bar touch-fill, no queue model)",
        "bars": len(bars), "span": f"{bars[0][0]} → {bars[-1][0]}",
        "params": {"bid_spread_bps": bid_bps, "ask_spread_bps": ask_bps,
                   "order_amt": order_amt, "inventory_skew": inv_skew,
                   "fee_bps": fee_bps, "refresh_bars": refresh},
        "fills_buy": fills_buy, "fills_sell": fills_sell,
        "total_fees_paid_bps_notional": round((fills_buy + fills_sell) * fee * order_amt * start_mid, 2),
        "end_inventory_btc": round(inventory, 4), "end_cash": round(cash, 2),
        "pnl_quote": round(final - quote_cash - base_inv * start_mid, 2),
        "buy_hold_pnl_quote": round((last - start_mid) * base_inv, 2),
        "inventory_range_btc": round(max(q["inv"] for q in quotes_log) - min(q["inv"] for q in quotes_log), 4) if quotes_log else 0,
        "sample_fills": quotes_log[:3] + quotes_log[-3:],
        "caveat": "触及即成交假设，无排队/逆向选择模型——真实做市 PnL 通常低于此估计",
        "fetched_at": dt.datetime.now().isoformat(timespec="seconds"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--params", default="{}")
    args = ap.parse_args()
    data = json.load(open(args.data))
    symbol, bars = next(iter(data.items()))
    p = json.loads(args.params)
    out = simulate(bars,
                   float(p.get("bid_spread_bps", 10)), float(p.get("ask_spread_bps", 10)),
                   float(p.get("order_btc", 0.01)), float(p.get("inventory_skew", 0.5)),
                   float(p.get("fee_bps", 2)), float(p.get("base_inventory_btc", 0.0)),
                   float(p.get("base_quote_cash", 100000)))
    out["symbol"] = symbol
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
