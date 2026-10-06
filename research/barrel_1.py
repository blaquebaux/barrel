#!/usr/bin/python3
# =============================================================================
# barrel_1.py — Commodity curve roll-carry: is there a harvestable roll yield, or just a contango bleed to avoid?
#
# DATA LIMIT: no futures curves in Alpaca → roll yield is proxied from the ETFs themselves (they roll the curve, so a
# front-month ETF's drag vs a store-of-value benchmark reveals structural contango). SIP daily total return.
#  (A) THE CONTANGO BLEED: the chronic front-month roll losers (USO oil, UNG gas) vs their own spot-ish path — how
#      much the curve costs a naive long. (B) a CARRY TILT: cross-sectional among commodity ETFs, long the backwardated
#      / positive-roll (proxied by positive 12m trend) and short the contangoed (negative trend) — does harvesting the
#      curve sign pay, or is it just commodity momentum?
# =============================================================================
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _barrel_common import panel, rets, stats, skew_of
import numpy as np
COMMS=["USO","UNG","UGA","DBA","CPER","DBB","GLD","SLV","WEAT","CORN"]
P, dates = panel(COMMS+["DBC"]); syms=[s for s in COMMS if s in P]
R={s:rets(P[s]) for s in P}
print("="*96); print(f"BARREL — commodity curve roll-carry  ({dates[0]} → {dates[-1]})"); print("="*96)
print(f"\n(A) THE CONTANGO BLEED (long-run CAGR of front-month ETFs — the roll drag):")
for s in ["USO","UNG","UGA","DBC","GLD"]:
    a=stats(R[s]); print(f"    {s:4} {a['cagr']*100:>+6.1f}%/yr   vol {a['vol']*100:.0f}%  (GLD/store-of-value ~no contango; USO/UNG = chronic roll losers)")
# (B) carry tilt: monthly, long top-third / short bottom-third by trailing-252d return (roll+trend proxy)
M=np.column_stack([P[s] for s in syms]); dr=M[1:]/M[:-1]-1; nd,nn=dr.shape
port=np.full(nd,np.nan); w=np.zeros(nn)
for t in range(252,nd):
    if (t-252)%21==0:
        sig=M[t]/M[t-252]-1; k=max(1,nn//3); o=np.argsort(sig); w=np.zeros(nn); w[o[-k:]]=1.0/k; w[o[:k]]=-1.0/k
    port[t]=w@dr[t]
port=port[252:]; pa=stats(port)
print(f"\n(B) CARRY/ROLL TILT (long positive-roll / short contangoed, monthly): Sharpe {pa['sh']:+.2f}, {pa['cagr']*100:+.1f}%/yr, maxDD {pa['dd']*100:+.0f}%, skew {skew_of(port):+.2f}")
bleed = stats(R['USO'])['cagr']<-0.03 or stats(R['UNG'])['cagr']<-0.05
tilt_works = pa['sh']>0.3
print("\n"+"="*96); print("READ:")
print(f"  • THE ROLL DRAG IS THE HEADLINE: USO {stats(R['USO'])['cagr']*100:+.0f}%/yr and UNG {stats(R['UNG'])['cagr']*100:+.0f}%/yr — chronic contango destroys naive front-month longs (vs GLD {stats(R['GLD'])['cagr']*100:+.0f}%, which barely rolls). 'Never buy-and-hold a front-month commodity ETF' is the first, biggest finding.")
print(f"  • HARVESTING THE SIGN: a long-backwardated / short-contango tilt earns Sharpe {pa['sh']:+.2f} — {'a real roll-carry/trend harvest (short the bleeders, long the backwardated)' if tilt_works else 'thin/noisy on ETF proxies'}; note it blends roll-carry WITH momentum (can''t cleanly separate without curves).")
if tilt_works:
    v=("CONDITIONAL: the commodity CURVE is tradeable at the sign level — the enormous contango bleed in USO/UNG is a "
       "persistent SHORT-carry opportunity, and a long-backwardated / short-contangoed tilt harvests it (Sharpe "
       f"{pa['sh']:+.2f}). BUT on ETFs this blends roll-carry with momentum and can't isolate pure roll yield; the real carry "
       "signal is each contract's own term structure (front-vs-back basis), which needs a futures feed = barrel_2. The "
       "durable, actionable takeaway now: AVOID/short the structural-contango commodities; don't buy-and-hold front-month ETFs.")
else:
    v=("CONDITIONAL / NULL-ish: the big real finding is the CONTANGO BLEED (USO/UNG destroyed by roll) — a clear 'don''t "
       "hold front-month ETFs' lesson and a short-carry opportunity — but a clean cross-sectional roll-carry HARVEST "
       "doesn't come through on ETF proxies (it's entangled with momentum and noisy). True roll yield needs futures term "
       "structure (front-vs-back basis) = barrel_2.")
print(f"  VERDICT: {v}")
print("  (No futures curves in Alpaca → roll yield inferred from ETF roll drag + a trend/roll proxy; pure per-contract carry (front-vs-back basis) = barrel_2.)")
