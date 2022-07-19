import uvicorn
from fastapi import FastAPI, Depends
from webhook import tradingview
from routes import exchange_route, quotation_route


def create_app():
    app = FastAPI()
    
    app.include_router(exchange_route.router, tags=["Exchange"], prefix="/api")
    app.include_router(quotation_route.router, tags=["Quotation"], prefix="/api")
    app.include_router(tradingview.router, tags=["WebHook"])
    return app


app = create_app()

@app.get("/")
def read_root():
    return {"Hello" : "World"}

if __name__ == '__main__':
    # uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True)
    uvicorn.run('main:app', host='141.164.48.85', port=80, reload=True)