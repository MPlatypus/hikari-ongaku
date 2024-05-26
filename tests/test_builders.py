# ruff: noqa: D100, D101, D102, D103

import datetime
import typing

import hikari
import pytest

from ongaku.abc.errors import SeverityType
from ongaku.abc.events import TrackEndReasonType
from ongaku.abc.routeplanner import IPBlockType
from ongaku.abc.routeplanner import RoutePlannerType
from ongaku.builders import EntityBuilder

PayloadT: typing.TypeAlias = typing.Final[
    typing.Mapping[str, typing.Any] | typing.Sequence[typing.Any]
]

GUILD_ID: typing.Final[str] = "1234567890"

TRACK_INFO_PAYLOAD: PayloadT = {
    "identifier": "identifier",
    "isSeekable": False,
    "author": "author",
    "length": 1,
    "isStream": True,
    "position": 2,
    "title": "title",
    "sourceName": "source_name",
    "uri": "uri",
    "artworkUrl": "artwork_url",
    "isrc": "isrc",
}

TRACK_PAYLOAD: PayloadT = {
    "encoded": "encoded",
    "info": TRACK_INFO_PAYLOAD,
    "pluginInfo": {},
    "userData": {},
}

PLAYER_STATE_PAYLOAD: PayloadT = {
    "time": 1,
    "position": 2,
    "connected": True,
    "ping": 3,
}

PLAYER_VOICE_PAYLOAD: PayloadT = {
    "token": "token",
    "endpoint": "endpoint",
    "sessionId": "session_id",
}

PLAYER_PAYLOAD: PayloadT = {
    "guildId": GUILD_ID,
    "track": TRACK_PAYLOAD,
    "volume": 1,
    "paused": True,
    "state": PLAYER_STATE_PAYLOAD,
    "voice": PLAYER_VOICE_PAYLOAD,
    "filters": {},
}

REST_ERROR_PAYLOAD: PayloadT = {
    "timestamp": 1,
    "status": 2,
    "error": "error",
    "message": "message",
    "path": "path",
    "trace": "trace",
}

EXCEPTION_ERROR_PAYLOAD: PayloadT = {
    "message": "message",
    "severity": "common",
    "cause": "cause",
}

READY_PAYLOAD: PayloadT = {"resumed": False, "sessionId": "session_id"}

PLAYER_UPDATE_PAYLOAD: PayloadT = {
    "guildId": GUILD_ID,
    "state": PLAYER_STATE_PAYLOAD,
}

WEBSOCKET_CLOSED_PAYLOAD: PayloadT = {
    "guildId": GUILD_ID,
    "code": 1,
    "reason": "reason",
    "byRemote": False,
}

TRACK_START_PAYLOAD: PayloadT = {"guildId": GUILD_ID, "track": TRACK_PAYLOAD}

TRACK_END_PAYLOAD: PayloadT = {
    "guildId": GUILD_ID,
    "track": TRACK_PAYLOAD,
    "reason": "finished",
}

TRACK_EXCEPTION_PAYLOAD: PayloadT = {
    "guildId": GUILD_ID,
    "track": TRACK_PAYLOAD,
    "exception": EXCEPTION_ERROR_PAYLOAD,
}

TRACK_STUCK_PAYLOAD: PayloadT = {
    "guildId": GUILD_ID,
    "track": TRACK_PAYLOAD,
    "thresholdMs": 1,
}

INFO_VERSION_PAYLOAD: PayloadT = {
    "semver": "semver",
    "major": 1,
    "minor": 2,
    "patch": 3,
    "preRelease": "pre_release",
    "build": "build",
}

INFO_GIT_PAYLOAD: PayloadT = {"branch": "branch", "commit": "commit", "commitTime": 1}

INFO_PLUGIN_PAYLOAD: PayloadT = {"name": "name", "version": "version"}

INFO_PAYLOAD: PayloadT = {
    "version": INFO_VERSION_PAYLOAD,
    "buildTime": 1,
    "git": INFO_GIT_PAYLOAD,
    "jvm": "jvm",
    "lavaplayer": "lavaplayer",
    "sourceManagers": ["source_manager_1", "source_manager_2"],
    "filters": ["filter_1", "filter_2"],
    "plugins": [INFO_PLUGIN_PAYLOAD],
}


PLAYLIST_INFO_PAYLOAD: PayloadT = {"name": "name", "selectedTrack": 1}

PLAYLIST_PAYLOAD: PayloadT = {
    "info": PLAYLIST_INFO_PAYLOAD,
    "pluginInfo": {},
    "tracks": [TRACK_PAYLOAD],
}

ROUTEPLANNER_FAILING_ADDRESS_PAYLOAD: PayloadT = {
    "failingAddress": "failing_address",
    "failingTimestamp": 1,
    "failingTime": "failing_time",
}

ROUTEPLANNER_IP_BLOCK_PAYLOAD: PayloadT = {"type": "Inet4Address", "size": "size"}

ROUTEPLANNER_DETAILS_PAYLOAD: PayloadT = {
    "ipBlock": ROUTEPLANNER_IP_BLOCK_PAYLOAD,
    "failingAddresses": [ROUTEPLANNER_FAILING_ADDRESS_PAYLOAD],
    "rotateIndex": "rotate_index",
    "ipIndex": "ip_index",
    "currentAddress": "current_address",
    "currentAddressIndex": "current_address_index",
    "blockIndex": "block_index",
}

ROUTEPLANNER_STATUS_PAYLOAD: PayloadT = {
    "class": "RotatingIpRoutePlanner",
    "details": ROUTEPLANNER_DETAILS_PAYLOAD,
}

SESSION_PAYLOAD: PayloadT = {"resuming": True, "timeout": 1}

STATISTICS_MEMORY_PAYLOAD: PayloadT = {
    "free": 1,
    "used": 2,
    "allocated": 3,
    "reservable": 4,
}

STATISTICS_CPU_PAYLOAD: PayloadT = {"cores": 1, "systemLoad": 2.3, "lavalinkLoad": 4.5}

STATISTICS_FRAME_STATS_PAYLOAD: PayloadT = {"sent": 1, "nulled": 2, "deficit": 3}

STATISTICS_PAYLOAD: PayloadT = {
    "players": 1,
    "playingPlayers": 2,
    "uptime": 3,
    "memory": STATISTICS_MEMORY_PAYLOAD,
    "cpu": STATISTICS_CPU_PAYLOAD,
    "frameStats": STATISTICS_FRAME_STATS_PAYLOAD,
}


@pytest.fixture
def builder() -> EntityBuilder:
    return EntityBuilder()


class TestBuilderErrors:
    def test_build_rest_error(self, builder: EntityBuilder):
        parsed_result = builder.build_rest_error(REST_ERROR_PAYLOAD)

        assert parsed_result.timestamp == datetime.datetime.fromtimestamp(1 / 1000)
        assert parsed_result.status == 2
        assert parsed_result.error == "error"
        assert parsed_result.message == "message"
        assert parsed_result.path == "path"
        assert parsed_result.trace == "trace"

    def test_build_exception_error(self, builder: EntityBuilder):
        parsed_result = builder.build_exception_error(EXCEPTION_ERROR_PAYLOAD)

        assert parsed_result.message == "message"
        assert parsed_result.severity == SeverityType.COMMON
        assert parsed_result.cause == "cause"


class TestBuilderEvents:
    def test_build_ready(self, builder: EntityBuilder):
        parsed_result = builder.build_ready(READY_PAYLOAD)

        assert parsed_result.resumed is False
        assert parsed_result.session_id == "session_id"

    def test_build_player_update(self, builder: EntityBuilder):
        parsed_result = builder.build_player_update(PLAYER_UPDATE_PAYLOAD)

        assert isinstance(parsed_result.guild_id, hikari.Snowflake)
        assert parsed_result.guild_id == hikari.Snowflake(1234567890)
        assert parsed_result.state == builder.build_player_state(PLAYER_STATE_PAYLOAD)

    def test_build_websocket_closed(self, builder: EntityBuilder):
        parsed_result = builder.build_websocket_closed(WEBSOCKET_CLOSED_PAYLOAD)

        assert isinstance(parsed_result.guild_id, hikari.Snowflake)
        assert parsed_result.guild_id == hikari.Snowflake(1234567890)
        assert parsed_result.code == 1
        assert parsed_result.reason == "reason"
        assert parsed_result.by_remote is False

    def test_build_track_start(self, builder: EntityBuilder):
        parsed_result = builder.build_track_start(TRACK_START_PAYLOAD)

        assert isinstance(parsed_result.guild_id, hikari.Snowflake)
        assert parsed_result.guild_id == hikari.Snowflake(1234567890)
        assert parsed_result.track == builder.build_track(TRACK_PAYLOAD)

    def test_build_track_end(self, builder: EntityBuilder):
        parsed_result = builder.build_track_end(TRACK_END_PAYLOAD)

        assert isinstance(parsed_result.guild_id, hikari.Snowflake)
        assert parsed_result.guild_id == hikari.Snowflake(1234567890)
        assert parsed_result.track == builder.build_track(TRACK_PAYLOAD)
        assert parsed_result.reason == TrackEndReasonType.FINISHED

    def test_build_track_exception(self, builder: EntityBuilder):
        parsed_result = builder.build_track_exception(TRACK_EXCEPTION_PAYLOAD)

        assert isinstance(parsed_result.guild_id, hikari.Snowflake)
        assert parsed_result.guild_id == hikari.Snowflake(1234567890)
        assert parsed_result.track == builder.build_track(TRACK_PAYLOAD)
        assert parsed_result.exception == builder.build_exception_error(
            EXCEPTION_ERROR_PAYLOAD
        )

    def test_build_track_stuck(self, builder: EntityBuilder):
        parsed_result = builder.build_track_stuck(TRACK_STUCK_PAYLOAD)

        assert isinstance(parsed_result.guild_id, hikari.Snowflake)
        assert parsed_result.guild_id == hikari.Snowflake(1234567890)
        assert parsed_result.track == builder.build_track(TRACK_PAYLOAD)
        assert parsed_result.threshold_ms == 1


class TestBuilderInfo:
    def test_build_info(self, builder: EntityBuilder):
        parsed_result = builder.build_info(INFO_PAYLOAD)

        assert parsed_result.version == builder.build_info_version(INFO_VERSION_PAYLOAD)
        assert parsed_result.build_time == datetime.datetime.fromtimestamp(1 / 1000)
        assert parsed_result.git == builder.build_info_git(INFO_GIT_PAYLOAD)
        assert parsed_result.jvm == "jvm"
        assert parsed_result.lavaplayer == "lavaplayer"
        assert parsed_result.source_managers == ["source_manager_1", "source_manager_2"]
        assert parsed_result.filters == ["filter_1", "filter_2"]
        assert parsed_result.plugins == [builder.build_info_plugin(INFO_PLUGIN_PAYLOAD)]

    def test_build_info_version(self, builder: EntityBuilder):
        parsed_result = builder.build_info_version(INFO_VERSION_PAYLOAD)

        assert parsed_result.semver == "semver"
        assert parsed_result.major == 1
        assert parsed_result.minor == 2
        assert parsed_result.patch == 3
        assert parsed_result.pre_release == "pre_release"
        assert parsed_result.build == "build"

    def test_build_info_git(self, builder: EntityBuilder):
        parsed_result = builder.build_info_git(INFO_GIT_PAYLOAD)

        assert parsed_result.branch == "branch"
        assert parsed_result.commit == "commit"
        assert parsed_result.commit_time == datetime.datetime.fromtimestamp(1 / 1000)

    def test_build_info_plugin(self, builder: EntityBuilder):
        parsed_result = builder.build_info_plugin(INFO_PLUGIN_PAYLOAD)

        assert parsed_result.name == "name"
        assert parsed_result.version == "version"


class TestBuilderPlayer:
    def test_build_player(self, builder: EntityBuilder):
        parsed_result = builder.build_player(PLAYER_PAYLOAD)

        assert isinstance(parsed_result.guild_id, hikari.Snowflake)
        assert parsed_result.guild_id == hikari.Snowflake(1234567890)
        assert parsed_result.track == builder.build_track(TRACK_PAYLOAD)
        assert parsed_result.volume == 1
        assert parsed_result.is_paused is True
        assert parsed_result.state == builder.build_player_state(PLAYER_STATE_PAYLOAD)
        assert parsed_result.voice == builder.build_player_voice(PLAYER_VOICE_PAYLOAD)
        assert parsed_result.filters == {}

    def test_build_player_state(self, builder: EntityBuilder):
        parsed_result = builder.build_player_state(PLAYER_STATE_PAYLOAD)

        assert parsed_result.time == datetime.datetime.fromtimestamp(1 / 1000)
        assert parsed_result.position == 2
        assert parsed_result.connected is True
        assert parsed_result.ping == 3

    def test_build_player_voice(self, builder: EntityBuilder):
        parsed_result = builder.build_player_voice(PLAYER_VOICE_PAYLOAD)

        assert parsed_result.token == "token"
        assert parsed_result.endpoint == "endpoint"
        assert parsed_result.session_id == "session_id"


class TestBuilderPlaylist:
    def test_build_playlist(self, builder: EntityBuilder):
        parsed_result = builder.build_playlist(PLAYLIST_PAYLOAD)

        assert parsed_result.info == builder.build_playlist_info(PLAYLIST_INFO_PAYLOAD)
        assert parsed_result.plugin_info == {}
        assert isinstance(parsed_result.tracks, typing.Sequence)
        assert len(parsed_result.tracks) == 1
        assert parsed_result.tracks[0] == builder.build_track(TRACK_PAYLOAD)

    def test_build_playlist_info(self, builder: EntityBuilder):
        parsed_result = builder.build_playlist_info(PLAYLIST_INFO_PAYLOAD)

        assert parsed_result.name == "name"
        assert parsed_result.selected_track == 1


class TestBuilderRoutePlanner:
    def test_build_routeplanner_status(self, builder: EntityBuilder):
        parsed_result = builder.build_routeplanner_status(ROUTEPLANNER_STATUS_PAYLOAD)

        assert parsed_result.cls == RoutePlannerType.ROTATING_ROUTE_PLANNER
        assert parsed_result.details == builder.build_routeplanner_details(
            ROUTEPLANNER_DETAILS_PAYLOAD
        )

    def test_build_routeplanner_details(self, builder: EntityBuilder):
        parsed_result = builder.build_routeplanner_details(ROUTEPLANNER_DETAILS_PAYLOAD)

        assert parsed_result.ip_block == builder.build_routeplanner_ipblock(
            ROUTEPLANNER_IP_BLOCK_PAYLOAD
        )
        assert isinstance(parsed_result.failing_addresses, typing.Sequence)
        assert len(parsed_result.failing_addresses) == 1
        assert parsed_result.failing_addresses[
            0
        ] == builder.build_routeplanner_failing_address(
            ROUTEPLANNER_FAILING_ADDRESS_PAYLOAD
        )
        assert parsed_result.rotate_index == "rotate_index"
        assert parsed_result.ip_index == "ip_index"
        assert parsed_result.current_address == "current_address"
        assert parsed_result.current_address_index == "current_address_index"
        assert parsed_result.block_index == "block_index"

    def test_build_ip_block(self, builder: EntityBuilder):
        parsed_result = builder.build_routeplanner_ipblock(
            ROUTEPLANNER_IP_BLOCK_PAYLOAD
        )

        assert parsed_result.type == IPBlockType.INET_4_ADDRESS
        assert parsed_result.size == "size"

    def test_build_failing_address(self, builder: EntityBuilder):
        parsed_result = builder.build_routeplanner_failing_address(
            ROUTEPLANNER_FAILING_ADDRESS_PAYLOAD
        )

        assert parsed_result.address == "failing_address"
        assert parsed_result.timestamp == datetime.datetime.fromtimestamp(1 / 1000)
        assert parsed_result.time == "failing_time"


class TestBuilderSession:
    def test_build_session(self, builder: EntityBuilder):
        parsed_result = builder.build_session(SESSION_PAYLOAD)

        assert parsed_result.resuming is True
        assert parsed_result.timeout == 1


class TestBuilderStatistics:
    def test_build_statistics(self, builder: EntityBuilder):
        parsed_result = builder.build_statistics(STATISTICS_PAYLOAD)

        assert parsed_result.players == 1
        assert parsed_result.playing_players == 2
        assert parsed_result.uptime == 3
        assert parsed_result.memory == builder.build_statistics_memory(
            STATISTICS_MEMORY_PAYLOAD
        )
        assert parsed_result.cpu == builder.build_statistics_cpu(STATISTICS_CPU_PAYLOAD)
        assert parsed_result.frame_stats == builder.build_statistics_frame_statistics(
            STATISTICS_FRAME_STATS_PAYLOAD
        )

    def test_build_statistics_memory(self, builder: EntityBuilder):
        parsed_result = builder.build_statistics_memory(STATISTICS_MEMORY_PAYLOAD)

        assert parsed_result.free == 1
        assert parsed_result.used == 2
        assert parsed_result.allocated == 3
        assert parsed_result.reservable == 4

    def test_build_statistics_cpu(self, builder: EntityBuilder):
        parsed_result = builder.build_statistics_cpu(STATISTICS_CPU_PAYLOAD)

        assert parsed_result.cores == 1
        assert parsed_result.system_load == 2.3
        assert parsed_result.lavalink_load == 4.5

    def test_build_statistics_frame_stats(self, builder: EntityBuilder):
        parsed_result = builder.build_statistics_frame_statistics(
            STATISTICS_FRAME_STATS_PAYLOAD
        )

        assert parsed_result.sent == 1
        assert parsed_result.nulled == 2
        assert parsed_result.deficit == 3


class TestBuilderTrack:
    def test_track(self, builder: EntityBuilder):
        parsed_result = builder.build_track(TRACK_PAYLOAD)

        assert parsed_result.encoded == "encoded"
        assert parsed_result.info == builder.build_track_info(TRACK_INFO_PAYLOAD)
        assert parsed_result.plugin_info == {}
        assert parsed_result.user_data == {}
        assert parsed_result.requestor is None

    def test_build_track_info(self, builder: EntityBuilder):
        parsed_result = builder.build_track_info(TRACK_INFO_PAYLOAD)

        assert parsed_result.identifier == "identifier"
        assert parsed_result.is_seekable is False
        assert parsed_result.author == "author"
        assert parsed_result.length == 1
        assert parsed_result.is_stream is True
        assert parsed_result.position == 2
        assert parsed_result.title == "title"
        assert parsed_result.source_name == "source_name"
        assert parsed_result.uri == "uri"
        assert parsed_result.artwork_url == "artwork_url"
        assert parsed_result.isrc == "isrc"
