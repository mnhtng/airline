from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom handler để format lại thông báo lỗi validation từ Pydantic
    Loại bỏ prefix "Value error, " không cần thiết
    """

    errors = []
    for error in exc.errors():
        if error["type"] == "value_error":
            # Loại bỏ "Value error, " từ message
            msg = error["msg"]
            if msg.startswith("Value error, "):
                msg = msg[13:]  # Bỏ 13 ký tự đầu "Value error, "
            errors.append(
                {
                    "field": " -> ".join(str(x) for x in error["loc"]),
                    "message": msg + ".",
                }
            )
        else:
            errors.append(
                {
                    "field": " -> ".join(str(x) for x in error["loc"]),
                    "message": error["msg"] + ".",
                }
            )

    return JSONResponse(
        status_code=422, content={"detail": "Dữ liệu không hợp lệ!", "errors": errors}
    )
