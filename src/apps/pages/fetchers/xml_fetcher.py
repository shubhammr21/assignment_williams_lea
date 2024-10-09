import requests

from ..exceptions import XMLFetchError  # noqa: TID252


class XMLFetcher:
    @staticmethod
    def fetch(url: str, timeout: int = 10) -> bytes:
        """Fetch XML content from a URL and return it. Raises an exception if
        the request fails."""
        try:
            resp = requests.get(url, timeout=timeout)
            resp.raise_for_status()
        except requests.HTTPError as e:
            msg = f"Error fetching XML: {e}"
            raise XMLFetchError(msg) from e
        else:
            return resp.content
