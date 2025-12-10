from app.config import create_app
from app.routers import etf

app = create_app()

app.include_router(etf.router)