"""Constants for the Quran Browser integration."""

import logging
from typing import Final

DOMAIN: Final = "quran_browser"
BASE_API_URL: Final = "https://api.quran.com/api/v4"
ENDPOINT_CHAPTERS = "/chapters"
ENDPOINT_AUDIO_FILES = "/chapter_recitations/{reciter_id}"
ENDPOINT_GET_CHAPTER = "/chapter_recitations/"

LOGGER = logging.getLogger(__package__)
