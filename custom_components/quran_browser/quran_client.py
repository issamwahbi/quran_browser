from typing import Any, Dict, List

from aiohttp import ClientSession, ClientResponseError

from .const import BASE_API_URL, LOGGER, ENDPOINT_CHAPTERS, ENDPOINT_AUDIO_FILES


class QuranClientError(Exception):
    """Custom exception for QuranClient errors."""


class QuranClient:
    """Client for interacting with the Quran API."""

    def __init__(self, session: ClientSession, user_agent: str) -> None:
        """Initialize the QuranClient."""
        self._session = session
        self._user_agent = user_agent

    async def fetch_chapter(self, reciter_id: int, chapter_id: int) -> Dict[str, Any]:
        """Fetches a single Quran chapter by ID."""
        url = f"{BASE_API_URL}{ENDPOINT_CHAPTERS}/{reciter_id}/{chapter_id}"
        headers = {"User-Agent": self._user_agent}

        try:
            async with self._session.get(url, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                return data.get("audio_file", {})
        except ClientResponseError as err:
            LOGGER.error("Error fetching chapter %d: %s", chapter_id, err)
            raise QuranClientError("Failed to fetch chapter") from err

    async def fetch_chapters(self) -> List[Dict[str, Any]]:
        """Fetches a list of Quran chapters."""
        url = f"{BASE_API_URL}{ENDPOINT_CHAPTERS}"
        headers = {"User-Agent": self._user_agent}

        try:
            async with self._session.get(url, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                return data.get("chapters", [])
        except ClientResponseError as err:
            LOGGER.error("Error fetching chapters: %s", err)
            raise QuranClientError("Failed to fetch chapters") from err

    async def fetch_audio_files(self, reciter_id: int) -> List[Dict[str, Any]]:
        """Fetches a list of audio files for a given reciter by ID."""
        url = f"{BASE_API_URL}{ENDPOINT_AUDIO_FILES.format(reciter_id=reciter_id)}"
        headers = {"User-Agent": self._user_agent}

        try:
            async with self._session.get(url, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                return data.get("audio_files", [])
        except ClientResponseError as err:
            LOGGER.error("Error fetching audio files for reciter %d: %s", reciter_id, err)
            raise QuranClientError("Failed to fetch audio files") from err
