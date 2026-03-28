from fastapi import APIRouter, HTTPException

from .mock_data import MARKET_INDICES
from .models import MarketIndex

router = APIRouter(prefix="/api/v1", tags=["Market Indices"])


@router.get("/indices", response_model=list[MarketIndex])
def list_indices() -> list[dict]:
    """Return snapshots for all tracked market indices."""
    return list(MARKET_INDICES.values())


@router.get("/indices/{symbol}", response_model=MarketIndex)
def get_index(symbol: str) -> dict:
    """Return a snapshot for a single market index by symbol."""
    key = symbol.upper()
    if key not in MARKET_INDICES:
        raise HTTPException(status_code=404, detail=f"Index '{key}' not found")
    return MARKET_INDICES[key]
