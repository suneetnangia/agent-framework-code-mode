from pydantic import BaseModel


class StockQuote(BaseModel):
    ticker: str
    name: str
    price: float
    change: float
    change_percent: float
    volume: int
    market_cap: int
    timestamp: str


class PortfolioHolding(BaseModel):
    ticker: str
    name: str
    quantity: int
    avg_cost: float
    current_price: float
    market_value: float
    unrealized_pnl: float
    sector: str
    allocation_percent: float


class PortfolioSummary(BaseModel):
    total_market_value: float
    total_unrealized_pnl: float
    holdings_count: int


class PortfolioResponse(BaseModel):
    summary: PortfolioSummary
    holdings: list[PortfolioHolding]


class MarketIndex(BaseModel):
    name: str
    symbol: str
    value: float
    change: float
    change_percent: float
    timestamp: str
