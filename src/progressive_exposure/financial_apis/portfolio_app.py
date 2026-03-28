import uvicorn
from fastapi import FastAPI

from .portfolio_router import router

app = FastAPI(
    title="Portfolio Holdings API",
    description="Mock portfolio holdings with sector allocation and P&L.",
    version="1.0.0",
)

app.include_router(router)


def main() -> None:
    uvicorn.run(
        "progressive_exposure.financial_apis.portfolio_app:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
    )


if __name__ == "__main__":
    main()
