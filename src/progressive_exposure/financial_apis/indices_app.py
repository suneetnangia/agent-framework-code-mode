import uvicorn
from fastapi import FastAPI

from .indices_router import router

app = FastAPI(
    title="Market Indices API",
    description="Mock market index snapshots for S&P 500, NASDAQ, and Dow Jones.",
    version="1.0.0",
)

app.include_router(router)


def main() -> None:
    uvicorn.run(
        "progressive_exposure.financial_apis.indices_app:app",
        host="0.0.0.0",
        port=8003,
        reload=True,
    )


if __name__ == "__main__":
    main()
