# dsh-hummingbot

> Pure market making, natively on DeepSeek Harness: spread quotes with inventory
> skew and a circuit breaker, running as a deterministic simulator on real 1m
> exchange data. **Caveats ride on every payload; live routing is guarded off.**
>
> Implements the core concept of [Hummingbot](https://github.com/hummingbot/hummingbot)
> (21.2k★, Apache-2.0); the upstream app joins in M2 as the live executor behind
> the family's fail-closed guard. Not affiliated.

**Status: name reserved — first release in development.**

Engine and docs: https://github.com/vicfei/dsh-hummingbot

- 48/48 balanced fills, inventory mean-reverting by design, on the first live smoke
- M1: queue/adverse-selection model, parameter sweeps; M2: guarded live execution
- Not investment advice.

---

**发布记录**：2026-11-17 owner 手动 `npm publish` 成功，latest=0.0.1，官方+镜像双验证。0.0.0-stage 为 staged-publishing 工件。
