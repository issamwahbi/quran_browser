"""Expose Favorite Radio Browser as a media source."""

from __future__ import annotations

import mimetypes

from radios import FilterBy, Order, RadioBrowser, Station

from homeassistant.components.media_player import MediaClass, MediaType
from homeassistant.components.media_source import (
    BrowseMediaSource,
    MediaSource,
    MediaSourceItem,
    PlayMedia,
    Unresolvable,
)
from homeassistant.core import HomeAssistant, callback

from . import RadioBrowserConfigEntry
from .const import DOMAIN

CODEC_TO_MIMETYPE = {
    "MP3": "audio/mpeg",
    "AAC": "audio/aac",
    "AAC+": "audio/aac",
    "OGG": "application/ogg",
}


async def async_get_media_source(hass: HomeAssistant) -> RadioMediaSource:
    """Set up Favorite Radio Browser media source."""
    # Radio browser supports only a single config entry
    entry = hass.config_entries.async_entries(DOMAIN)[0]

    return RadioMediaSource(hass, entry)


class RadioMediaSource(MediaSource):
    """Provide Favorite Radio stations as media sources."""

    name = "Favorite Radio Browser"

    def __init__(self, hass: HomeAssistant, entry: RadioBrowserConfigEntry) -> None:
        """Initialize RadioMediaSource."""
        super().__init__(DOMAIN)
        self.hass = hass
        self.entry = entry

    @property
    def radios(self) -> RadioBrowser:
        """Return the radio browser."""
        return self.entry.runtime_data

    async def async_resolve_media(self, item: MediaSourceItem) -> PlayMedia:
        """Resolve selected Favorite Radio station to a streaming URL."""
        radios = self.radios

        station = await radios.station(uuid=item.identifier)
        if not station:
            raise Unresolvable("Radio station is no longer available")

        if not (mime_type := self._async_get_station_mime_type(station)):
            raise Unresolvable("Could not determine stream type of radio station")

        # Register "click" with Radio Browser
        await radios.station_click(uuid=station.uuid)

        return PlayMedia(station.url, mime_type)

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
            can_play=False,
            can_expand=True,
            children=[
                *await self._async_build_by_country(radios, item),
            ],
        )

    @callback
    @staticmethod
    def _async_get_station_mime_type(station: Station) -> str | None:
        """Determine mime type of a favorite radio station."""
        mime_type = CODEC_TO_MIMETYPE.get(station.codec)
        if not mime_type:
            mime_type, _ = mimetypes.guess_type(station.url)
        return mime_type

    @callback
    def _async_build_stations(
        self, radios: RadioBrowser, stations: list[Station]
    ) -> list[BrowseMediaSource]:
        """Build list of media sources from favorite radio stations."""
        items: list[BrowseMediaSource] = []

        for station in stations:
            if station.codec == "UNKNOWN" or not (
                mime_type := self._async_get_station_mime_type(station)
            ):
                continue

            items.append(
                BrowseMediaSource(
                    domain=DOMAIN,
                    identifier=station.uuid,
                    media_class=MediaClass.MUSIC,
                    media_content_type=mime_type,
                    title=station.name,
                    can_play=True,
                    can_expand=False,
                    thumbnail=station.favicon,
                )
            )

        return items

    async def _async_build_by_country(
        self, radios: RadioBrowser, item: MediaSourceItem
    ) -> list[BrowseMediaSource]:
        """Handle browsing favorite radio stations by country."""
        country_code = "MA"
        stations = await radios.stations(
            filter_by=FilterBy.COUNTRY_CODE_EXACT,
            filter_term=country_code,
            hide_broken=True,
            order=Order.NAME,
            reverse=False,
        )
        return self._async_build_stations(radios, stations)
