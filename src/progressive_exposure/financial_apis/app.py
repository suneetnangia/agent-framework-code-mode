import uvicorn
from fastapi import FastAPI

from .indices_router import router as indices_router
from .portfolio_router import router as portfolio_router
from .stocks_router import router as stocks_router

app = FastAPI(
    title="Financial Data Services",
    description="Mock financial data APIs for stock quotes, portfolio holdings, and market indices.",
    version="1.0.0",
)

app.include_router(stocks_router)
app.include_router(portfolio_router)
app.include_router(indices_router)


def main() -> None:
    uvicorn.run(
        "progressive_exposure.financial_apis.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
