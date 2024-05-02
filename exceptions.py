from fastapi import status
from fastapi.responses import JSONResponse

async def validation_exception_handler(request, exc):
    """
    Exception handler for validation errors raised by FastAPI.

    Args:
        request: The request that triggered the validation error.
        exc (RequestValidationError): The validation error exception.

    Returns:
        JSONResponse: A JSON response containing details of the validation errors.
    """
    # Extract error details from the validation exception
    error_details = [error["msg"] for error in exc.errors()]
    
    # Create a JSON response with 400 status code and error details
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Validation error", "errors": error_details},
    )
