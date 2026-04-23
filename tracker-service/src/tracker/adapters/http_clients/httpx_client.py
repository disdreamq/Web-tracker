import logging

from httpx import (
    AsyncClient,
    ConnectError,
    InvalidURL,
    NetworkError,
    Response,
    TimeoutException,
)
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from src.core.exceptions import (
    PageConnectionError,
    PageFetchError,
    PageInvalidURLError,
    PageTimeoutError,
    UnexpectedException,
)
from src.interfaces.http_client_interface import IHTTPClientRepository

logger = logging.getLogger(__name__)


class BaseClient(IHTTPClientRepository):
    """
    HTTP client using httpx with retry logic.

    Fetches web pages with automatic retry on timeout and connection errors.
    """

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((PageTimeoutError, PageConnectionError)),
    )
    async def get(self, url: str) -> Response:
        """
        Fetch content from URL with automatic retry.

        Retries on timeout and connection errors (up to 3 attempts
        with exponential backoff).

        Args:
            url: URL to fetch.

        Returns:
            HTTP response with status code 200.

        Raises:
            PageTimeoutError: If request times out.
            PageConnectionError: If network error occurs.
            PageInvalidURLError: If URL is invalid.
            PageFetchError: If non-200 status code returned.
            UnexpectedException: If unexpected error occurs.

        Example:
            >>> client = BaseClient()
            >>> response = await client.get("https://example.com")
            >>> print(response.status_code)
            200
        """
        try:
            async with AsyncClient() as client:
                response = await client.get(url)
            if response.status_code != 200:
                raise PageFetchError(
                    "Page fetch error", status_code=response.status_code
                )
            return response
        except TimeoutException as e:
            raise PageTimeoutError(f"Timeout fetching {url}") from e
        except (ConnectError, NetworkError) as e:
            raise PageConnectionError(f"Network error fetching {url}") from e
        except InvalidURL as e:
            raise PageInvalidURLError(f"Invalid URL: {url}") from e
        except Exception as e:
            raise UnexpectedException(f"Unexpected error: {e}") from e
