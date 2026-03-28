from fastapi import APIRouter, HTTPException

from .mock_data import STOCK_QUOTES
from .models import StockQuote

router = APIRouter(prefix="/api/v1", tags=["Stock Quotes"])


@router.get("/stocks", response_model=list[StockQuote])
def list_stocks() -> list[dict]:
    """Return quotes for all available stocks."""
    return list(STOCK_QUOTES.values())


@router.get("/stocks/{ticker}", response_model=StockQuote)
def get_stock(ticker: str) -> dict:
    """Return a quote for a single stock by ticker symbol."""
    key = ticker.upper()
    if key not in STOCK_QUOTES:
        raise HTTPException(status_code=404, detail=f"Ticker '{key}' not found")
    return STOCK_QUOTES[key]
