from fastapi import middleware
from requests import Request

class HttpMiddleware:
    
    async def __call__(self, request: Request, call_next):
        print("MIDDLE WARE START")
        print(request.headers)
        print(request.cookies)
        print(request.client.host)
        response = await call_next(request)
        print(response)
        print("MIDDLE WARE END")
        return response