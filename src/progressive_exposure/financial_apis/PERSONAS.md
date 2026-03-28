# Finance Personas & API Chaining Scenarios

## Persona 1: Retail Investor

**Sarah, 35, tech employee with a 401k and brokerage account**

**Goal**: Understand how her portfolio is performing relative to the broader market.

### Prompts

- *"How is my portfolio doing compared to the S&P 500 today?"*
  - `GET /api/v1/portfolio` (total P&L) → `GET /api/v1/indices/SPX` (S&P change%) → compare

- *"Which of my holdings are dragging down my portfolio, and is it just my stocks or the whole market?"*
  - `GET /api/v1/portfolio` (find negative P&L holdings) → `GET /api/v1/stocks/{ticker}` per loser → `GET /api/v1/indices` (market context)

---

## Persona 2: Financial Advisor

**David, 48, independent wealth manager**

**Goal**: Quickly assess a client's risk exposure and sector concentration against market conditions.

### Prompts

- *"Show me the client's sector allocation and flag any sector that's overweight compared to current market performance."*
  - `GET /api/v1/portfolio` (sector allocations) → `GET /api/v1/indices` (sector-proxy benchmarks) → `GET /api/v1/stocks/{ticker}` for top holdings

- *"Give me a rebalancing summary — which positions are outsized and what's their current price action?"*
  - `GET /api/v1/portfolio` (allocation%) → `GET /api/v1/stocks/{ticker}` per holding (current price/change) → `GET /api/v1/indices` (market direction for timing)

---

## Persona 3: Risk Analyst

**Emily, 30, works at a hedge fund**

**Goal**: Assess portfolio sensitivity to market moves and identify correlated risk.

### Prompts

- *"If the NASDAQ drops 2% today, which of our holdings are most exposed?"*
  - `GET /api/v1/indices/IXIC` (NASDAQ current state) → `GET /api/v1/portfolio` (holdings list) → `GET /api/v1/stocks/{ticker}` per tech holding (check which are already declining)

- *"What's our total unrealized P&L and how does each position's daily move compare to its benchmark index?"*
  - `GET /api/v1/portfolio` (all holdings + P&L) → `GET /api/v1/stocks` (daily changes) → `GET /api/v1/indices` (benchmark changes) → compute relative performance
