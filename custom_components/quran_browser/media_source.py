"""Expose Quran Browser as a media source."""

from __future__ import annotations

from homeassistant.components.media_player import MediaClass, MediaType
from homeassistant.components.media_source import (
    BrowseMediaSource,
    MediaSource,
    MediaSourceItem,
    PlayMedia,
    Unresolvable,
)

from homeassistant.core import HomeAssistant

from .quran_client import QuranClient
from . import QuranBrowserConfigEntry
from .const import DOMAIN

async def async_get_media_source(hass: HomeAssistant) -> QuranMediaSource:
    """Set up Quran Browser media source."""
    entry = hass.config_entries.async_entries(DOMAIN)[0]

    return QuranMediaSource(hass, entry)

class QuranMediaSource(MediaSource):
    """Provide Quran stations as media sources."""

    name = "Quran Browser"

    def __init__(self, hass: HomeAssistant, entry: QuranBrowserConfigEntry) -> None:
        """Initialize RadioMediaSource."""
        super().__init__(DOMAIN)
        self.hass = hass
        self.entry = entry

    @property
    def quranClient(self) -> QuranClient:
        """Return the radio browser."""
        return self.entry.runtime_data

    async def async_resolve_media(self, item: MediaSourceItem) -> PlayMedia:
        """Resolve selected Quran station to a streaming URL."""
        quranClient = self.quranClient
        reciter_id = self.entry.data["reciter_id"]

        chapter = await quranClient.fetch_chapter(reciter_id=reciter_id, chapter_id=int(item.identifier))
        if not chapter:
            raise Unresolvable("Quran chapter not found")


        return PlayMedia(chapter.audio_url, "audio/mpeg")
    
    async def async_browse_media(
            self,
            item: MediaSourceItem,
        ) -> BrowseMediaSource:
            """Return media."""
            radios = self.radios

            return BrowseMediaSource(
                domain=DOMAIN,
                identifier=None,
                media_class=MediaClass.CHANNEL,
                media_content_type=MediaType.MUSIC,
                title=self.entry.title,
                can_play=True,
                can_expand=True,
            )

