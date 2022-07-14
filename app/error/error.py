

# class StatusCode:
#     """ 
#     HTTP Status를 재정의 
#     """
#     HTTP_500 = 500  
#     HTTP_400 = 400   
#     HTTP_401 = 401
#     HTTP_403 = 403
#     HTTP_404 = 404
#     HTTP_405 = 405
    
# class ErrCode:
#     """
#     에러에 대한 상태값을 정의
#     """
#     # ERR_0 : 알 수 없는 에러
#     ERR_0 = 0
#     # ERR_1000 : Bad Parameter. 파라미터가 잘못 입력된 경우
#     ERR_1000 = 1000 


# class APIException(Exception):
#     """_summary_
    
#     API 연동 시에 발생하는 Exception을 처리하기 위한 Base Class
    
#     Args:
#         Exception (_type_): _description_
#     """
#     status_code: int
#     code: int
#     msg: str
#     detail: str
#     ex: Exception
    
#     def __init__(
#         self,
#         status_code: int = StatusCode.HTTP_500,
#         code: int = ErrCode.ERR_0,
#         msg: str = None,
#         detail: str = None,
#         ex: Exception = None,
#     ):
#         """_summary_

#         Args:
#             status_code (int, optional): HTTP 상태 코드. Defaults to StatusCode.HTTP_500.
#             code (int, optional): 오류 코드. Defaults to ErrCode.ERR_0.
#             msg (str, optional): 오류 메시지. Defaults to None.
#             detail (str, optional): 상세 메시지. Defaults to None.
#             ex (Exception, optional): Exception 객체. Defaults to None.
#         """
#         self.status_code= status_code
#         self.code= code
#         self.msg= msg
#         self.detail= detail
#         self.ex= ex
#         super().__init__(ex)
        
        
# # BadParameterException
# class BadParameterException(APIException):
#     """_summary_

#     입력값이 잘못된 경우에 발생하는 Exception
    
#     Args:
#         APIException (_type_): _description_
#     """
#     def __init__(self):
#         super().__init__(
#             status_code= StatusCode.HTTP_400,
#             msg= f'전달값이 잘못되었습니다.',
#             detail= f'Parameter Error',
#             code= ErrCode.ERR_1000,
#             ex= None
#         )



from typing import Any


class BaseError(Exception):
    name: str
    code: int
    message: str
    
    def __init__(self, **ctx: Any) -> None:
        self.__dict__ = ctx

    def __str__(self) -> str:
        return self.msg.format(**self.__dict__)


class InvalidParamError(BaseError):
    name = "Invalid Param Error"
    code = 700
    message = "파라미터값이 잘못 되었습니다."
    
