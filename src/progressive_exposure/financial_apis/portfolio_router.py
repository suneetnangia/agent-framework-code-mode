from fastapi import APIRouter

from .mock_data import PORTFOLIO_HOLDINGS
from .models import PortfolioHolding, PortfolioResponse, PortfolioSummary

router = APIRouter(prefix="/api/v1", tags=["Portfolio Holdings"])


@router.get("/portfolio", response_model=PortfolioResponse)
def get_portfolio() -> dict:
    """Return all portfolio holdings with a summary of total value and P&L."""
    total_value = sum(h["market_value"] for h in PORTFOLIO_HOLDINGS)
    total_pnl = sum(h["unrealized_pnl"] for h in PORTFOLIO_HOLDINGS)
    return {
        "summary": PortfolioSummary(
            total_market_value=round(total_value, 2),
            total_unrealized_pnl=round(total_pnl, 2),
            holdings_count=len(PORTFOLIO_HOLDINGS),
        ),
        "holdings": [PortfolioHolding(**h) for h in PORTFOLIO_HOLDINGS],
    }
