import uvicorn
from fastapi import FastAPI, Depends
from routes import exchange_route

def create_app():
    app = FastAPI()
    
    app.include_router(exchange_route.router, tags=["Exchange"], prefix="/api")
    return app


app = create_app()

@app.get("/")
def read_root():
    return {"Hello" : "World"}

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True)