import uvicorn
from fastapi import FastAPI, Depends
from routes import account_route, order_route

def create_app():
    app = FastAPI()
    
    app.include_router(account_route.router, tags=["Account"], prefix="/api")
    app.include_router(order_route.router, tags=["Order"], prefix="/api")
    return app


app = create_app()

@app.get("/")
def read_root():
    return {"Hello" : "World"}

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True)