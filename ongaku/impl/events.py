# ruff: noqa: D101, D102

from __future__ import annotations

import hikari

from ongaku.abc import errors as errors_
from ongaku.abc import events as events_
from ongaku.abc import player as player_
from ongaku.abc import track as track_
from ongaku.enums import TrackEndReasonType


class Ready(events_.Ready):
    def __init__(self, resumed: bool, session_id: str) -> None:
        self._resumed = resumed
        self._session_id = session_id

    @property
    def resumed(self) -> bool:
        return self._resumed

    @property
    def session_id(self) -> str:
        return self._session_id


class PlayerUpdate(events_.PlayerUpdate):
    def __init__(self, guild_id: hikari.Snowflake, state: player_.State) -> None:
        self._guild_id = guild_id
        self._state = state

    @property
    def guild_id(self) -> hikari.Snowflake:
        return self._guild_id

    @property
    def state(self) -> player_.State:
        return self._state


class WebsocketClosed(events_.WebsocketClosed):
    def __init__(
        self, guild_id: hikari.Snowflake, code: int, reason: str, by_remote: bool
    ) -> None:
        self._guild_id = guild_id
        self._code = code
        self._reason = reason
        self._by_remote = by_remote

    @property
    def guild_id(self) -> hikari.Snowflake:
        return self._guild_id

    @property
    def code(self) -> int:
        return self._code

    @property
    def reason(self) -> str:
        return self._reason

    @property
    def by_remote(self) -> bool:
        return self._by_remote


class TrackStart(events_.TrackStart):
    def __init__(self, guild_id: hikari.Snowflake, track: track_.Track) -> None:
        self._guild_id = guild_id
        self._track = track

    @property
    def guild_id(self) -> hikari.Snowflake:
        return self._guild_id

    @property
    def track(self) -> track_.Track:
        return self._track


class TrackEnd(events_.TrackEnd):
    def __init__(
        self,
        guild_id: hikari.Snowflake,
        track: track_.Track,
        reason: TrackEndReasonType,
    ) -> None:
        self._guild_id = guild_id
        self._track = track
        self._reason = reason

    @property
    def guild_id(self) -> hikari.Snowflake:
        return self._guild_id

    @property
    def track(self) -> track_.Track:
        return self._track

    @property
    def reason(self) -> TrackEndReasonType:
        return self._reason


class TrackException(events_.TrackException):
    def __init__(
        self,
        guild_id: hikari.Snowflake,
        track: track_.Track,
        exception: errors_.ExceptionError,
    ) -> None:
        self._guild_id = guild_id
        self._track = track
        self._exception = exception

    @property
    def guild_id(self) -> hikari.Snowflake:
        return self._guild_id

    @property
    def track(self) -> track_.Track:
        return self._track

    @property
    def exception(self) -> errors_.ExceptionError:
        return self._exception


class TrackStuck(events_.TrackStuck):
    def __init__(
        self, guild_id: hikari.Snowflake, track: track_.Track, threshold_ms: int
    ) -> None:
        self._guild_id = guild_id
        self._track = track
        self._threshold_ms = threshold_ms

    @property
    def guild_id(self) -> hikari.Snowflake:
        return self._guild_id

    @property
    def track(self) -> track_.Track:
        return self._track

    @property
    def threshold_ms(self) -> int:
        return self._threshold_ms


class QueueEmpty(events_.QueueEmpty):
    def __init__(self, guild_id: hikari.Snowflake, old_track: track_.Track) -> None:
        self._guild_id = guild_id
        self._old_track = old_track

    @property
    def guild_id(self) -> hikari.Snowflake:
        return self._guild_id

    @property
    def old_track(self) -> track_.Track:
        return self._old_track


class QueueNext(events_.QueueNext):
    def __init__(
        self, guild_id: hikari.Snowflake, track: track_.Track, old_track: track_.Track
    ) -> None:
        self._guild_id = guild_id
        self._track = track
        self._old_track = old_track

    @property
    def guild_id(self) -> hikari.Snowflake:
        return self._guild_id

    @property
    def track(self) -> track_.Track:
        return self._track

    @property
    def old_track(self) -> track_.Track:
        return self._old_track