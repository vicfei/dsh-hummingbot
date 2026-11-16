---
name: dsh-hummingbot
description: Pure market-making simulator for DeepSeek Harness — spread quotes with inventory skew and circuit breaker on real 1m data; deterministic, caveats on every payload; live routing guarded off.
---

Use this skill when asked about market making ("做市能不能赚", "价差策略在 BTC 上
表现如何", inventory dynamics). The engine is deterministic — you parameterize,
it simulates.

## Run

```bash
KIT=<this-directory>
python3 $KIT/scripts/mm_sim.py --data <1m_klines.json> --params '{...}'
```

1m klines JSON: {"SYMBOL": [[datetime, open, close, high, low, volume], ...]} —
fetch via the family's ccxt bridge (relay if CN network).

## Discipline

- Always quote the caveat with results: touch-fill assumption overstates real MM PnL.
- Inventory imbalance is a risk metric — report end_inventory and range verbatim.
- Live routing stays guarded; enabling is a human act (M2, behind family guard).
- Not investment advice.
