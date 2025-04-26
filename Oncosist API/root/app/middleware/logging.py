"""
Logging middleware for FastAPI.

This module captures:
- Incoming request details (method, URL, JSON body if applicable).
- Outgoing response details (status code, response body if applicable).
- Processing time for each request.
"""

import logging
import json
import time
from datetime import datetime
from fastapi import Request, Response
from fastapi.responses import JSONResponse, StreamingResponse, PlainTextResponse
from starlette.middleware.base import BaseHTTPMiddleware
from colorama import Fore, Style, init

# Initialize colorama for colored logging output
init(autoreset=True)

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        logging.FileHandler("api_responses.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class CustomLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging requests and responses.

    Captures:
    - The incoming request (method, path, JSON body if possible).
    - The outgoing response (status code, JSON/Plain text).
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Middleware entry point that intercepts requests and responses.

        Args:
            request (Request): The incoming FastAPI request object.
            call_next (Callable): The next middleware or endpoint handler.

        Returns:
            Response: The processed response.
        """
        # Capture request details
        method = request.method
        url = str(request.url)

        # Attempt to read request body safely
        request_body = await request.body()
        try:
            request_json = json.loads(request_body.decode("utf-8")) if request_body else None
        except (json.JSONDecodeError, UnicodeDecodeError):
            request_json = None

        # Log request details
        request_log = (
            f"\n--- Incoming Request ---\n"
            f"{Fore.CYAN}Method:{Style.RESET_ALL} {method}\n"
            f"{Fore.CYAN}URL:{Style.RESET_ALL} {url}\n"
        )
        if request_json:
            request_log += f"{Fore.CYAN}Request JSON:{Style.RESET_ALL}\n{json.dumps(request_json, indent=4)}\n"
        request_log += "------------------------\n"
        logger.info(request_log)

        # Restore request body in scope for FastAPI after reading
        request.scope["body"] = request_body

        # Start processing timer
        start_time = time.time()

        # Process request and capture response
        response = await call_next(request)
        process_time = time.time() - start_time

        # Read response body safely
        response_body = b""
        if isinstance(response, (JSONResponse, PlainTextResponse)):
            response_body = response.body
        elif isinstance(response, StreamingResponse):
            response_body = b"Streaming Response"
        else:
            response_body = b"Skipped Non-JSON Response"

        # Convert response body to JSON safely
        try:
            response_json = json.loads(response_body.decode("utf-8")) if response_body else None
        except (json.JSONDecodeError, UnicodeDecodeError):
            response_json = None

        # Determine response status and description
        status_code = response.status_code
        description = "Successful Response" if status_code < 400 else "Error Response"

        # Set log color based on response status
        if 200 <= status_code < 300:
            color = Fore.GREEN
        elif 400 <= status_code < 500:
            color = Fore.YELLOW
        else:
            color = Fore.RED

        # Log response details
        log_message = (
            "\n--- Outgoing Response ---\n"
            f"{Fore.GREEN}Timestamp:{Style.RESET_ALL} {datetime.utcnow().isoformat()}\n"
            f"{color}Status Code:{Style.RESET_ALL} {status_code}\n"
            f"{color}Description:{Style.RESET_ALL} {description}\n"
        )
        if response_json:
            log_message += f"{color}Response:{Style.RESET_ALL}\n{json.dumps(response_json, indent=4)}\n"
        log_message += "-------------------------\n"

        logger.info(log_message)

        # Return response to client
        if isinstance(response, (JSONResponse, PlainTextResponse)):
            return Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )
        return response  # For streaming responses, return as is
