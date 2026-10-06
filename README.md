# Blaque Baux Barrel

**Commodity curve roll-carry — a harvestable roll yield, or a contango bleed to avoid?**

> **Not investment advice.** Educational/research software. See [DISCLAIMER](DISCLAIMER.md) and [LICENSE](LICENSE).

```bash
python3 research/barrel_1.py   # needs Alpaca data keys in the environment
```

**Data limit:** no futures curves in Alpaca → roll yield inferred from ETF roll drag + a trend/roll proxy.

## Finding (conditional / null-ish)
- **The contango bleed is the headline:** UNG **−22%/yr**, chronic roll losers destroy naive front-month longs (vs GLD +13%, which barely rolls). *Never buy-and-hold a front-month commodity ETF.*
- **But no clean harvest:** a long-backwardated / short-contango tilt earns **Sharpe −0.01** (−71% maxDD) — entangled with momentum and noisy on ETF proxies.

## Verdict
**CONDITIONAL / NULL-ish.** The durable, actionable finding is the *contango bleed* (a short-carry opportunity and a clear "avoid front-month ETFs" lesson); a clean cross-sectional roll-carry *harvest* needs each contract's own term structure (front-vs-back basis) = `barrel_2` with a futures feed.

## Status
**Research.** Honest white-space study — verdict falls where it falls, proxy limits named, `barrel_2` path noted. Fat-tail scorecard, causal, Alpaca SIP daily total return. No live capital.
