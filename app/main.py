import uvicorn
from fastapi import FastAPI, Depends, Request
from middlewares.http_middleware import HttpMiddleware
from webhook import tradingview
from routes import exchange_route, quotation_route
from starlette.middleware.base import BaseHTTPMiddleware

def create_app():
    app = FastAPI()
    
    app.include_router(exchange_route.router, tags=["Exchange"], prefix="/api")
    app.include_router(quotation_route.router, tags=["Quotation"], prefix="/api")
    app.include_router(tradingview.router, tags=["WebHook"])
    
    http_middleware = HttpMiddleware()
    app.add_middleware(BaseHTTPMiddleware, dispatch=http_middleware)
    return app


app = create_app()

@app.get("/")
def read_root():
    return {"Hello" : "World"}



if __name__ == '__main__':
    # uvicorn.run('main:app', host='localhost', port=8080, reload=True)
    uvicorn.run('main:app', host='141.164.48.85', port=80, reload=True)