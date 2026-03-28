import uvicorn
from fastapi import FastAPI

from .stocks_router import router

app = FastAPI(
    title="Stock Quotes API",
    description="Mock stock quote data for major tickers.",
    version="1.0.0",
)

app.include_router(router)


def main() -> None:
    uvicorn.run(
        "progressive_exposure.financial_apis.stocks_app:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
    )


if __name__ == "__main__":
    main()
