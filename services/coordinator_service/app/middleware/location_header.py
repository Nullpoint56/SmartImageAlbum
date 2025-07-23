from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class AbsoluteLocationHeaderMiddleware(BaseHTTPMiddleware):
    """
    Converts relative `Location` headers to absolute URLs
    using the incoming request's scheme and host.
    """
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        location = response.headers.get("Location")

        if location and location.startswith("/"):
            base_url = str(request.base_url).rstrip("/")
            response.headers["Location"] = f"{base_url}{location}"

        return response
