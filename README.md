# dsh-hummingbot — market making, natively on DeepSeek Harness

**Spread quotes around the mid, inventory-skewed, refreshed by the bar — a
deterministic pure-market-making engine running on real exchange data, with
honest caveats attached to every payload and live routing guarded off.**
**围绕中间价挂双边价差单、库存偏移、按 bar 刷新——跑在真实交易所数据上的
确定性纯做市引擎，偏差声明随载荷，实盘路由护栏锁死。**

[![DeepSeek Harness](https://img.shields.io/badge/DSH-plugin-4E6DD4)](https://github.com/deepseek-ai) [![License: MIT](https://img.shields.io/badge/license-MIT-3da639)](LICENSE) [![Hummingbot Apache-2.0](https://img.shields.io/badge/concept-Hummingbot%20Apache--2.0-ff9c41)](https://github.com/hummingbot/hummingbot)

> Implements the core concept of [Hummingbot](https://github.com/hummingbot/hummingbot)
> (21.2k★) — pure market making — as a native DSH engine; the heavy upstream app
> (Docker) joins in M2 as the live executor behind the family's fail-closed guard.
> Not affiliated. Family: [dsh-TradingAgents](https://github.com/vicfei/dsh-TradingAgents) ·
> [dsh-ai-hedge-fund](https://github.com/vicfei/dsh-ai-hedge-fund) ·
> [dsh-Vibe-Trading](https://github.com/vicfei/dsh-Vibe-Trading) ·
> [dsh-OpenBB](https://github.com/vicfei/dsh-OpenBB) · [dsh-CCXT](https://github.com/vicfei/dsh-CCXT) ·
> [dsh-nautilus_trader](https://github.com/vicfei/dsh-nautilus_trader).

## Why (Hummingbot exists — what does native add for DSH agents?)

| | Hummingbot app (Docker) | **dsh-hummingbot** |
|---|---|---|
| Runs where | its own container/CLI | **inside DSH** — agents parameterize and run MM sims in-session |
| Sim-first loop | production-first | **deterministic simulator on real 1m data**, caveats on every payload |
| Inventory logic | controllers (v2, real book) | spread-skew + **circuit breaker** (5× order-amount), mean-reverting by design |
| Live orders | bot runs live by default | **guarded off** — family fail-closed DNA; hummingbot wiring lands in M2 behind it |

## Quick start

```bash
git clone https://github.com/vicfei/dsh-hummingbot && cd dsh-hummingbot
python3 scripts/mm_sim.py --data <1m_klines.json> \
  --params '{"bid_spread_bps":15,"ask_spread_bps":15,"order_btc":0.02,"inventory_skew":0.5,"fee_bps":2}'
```

Real smoke (2026-11-16, binance BTC/USDT 500×1m via relay): **48 buys / 48 sells,
inventory mean-reverted to 0 (peak 4 order-lots), PnL −61 USDT** — at 15 bps spread
vs 2 bps taker fees, the edge is eaten: the simulator teaches parameter sensitivity
honestly. The first run caught a textbook skew **sign error** (485 buys / 0 sells —
quotes chasing inventory) — fixed, and the runaway case is now a circuit-breaker test.

## Status & roadmap

v0 pure-MM simulator smoke-tested on live data. [ROADMAP](ROADMAP.md): M1 order-book
queue/selection model + parameter sweeps; M2 hummingbot-docker as live executor
behind the family guard (backtest-gate + triple-arm, shared with dsh-CCXT).

## License & disclaimer

MIT; concept inspired by Apache-2.0 upstream — no upstream code used. Simulation
assumptions are stated on every payload. **Not investment advice.**
