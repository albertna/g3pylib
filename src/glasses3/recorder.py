import asyncio
from datetime import datetime
from types import NoneType
from typing import Awaitable, List, Optional, Tuple, cast

from glasses3.g3typing import URI, JSONObject, SignalBody
from glasses3.utils import APIComponent, EndpointKind
from glasses3.websocket import G3WebSocketClientProtocol


class Recorder(APIComponent):
    def __init__(self, connection: G3WebSocketClientProtocol, api_uri: URI) -> None:
        self._connection = connection
        super().__init__(api_uri)

    async def get_created(self) -> Optional[datetime]:
        response = await self._connection.require_get(
            self.generate_endpoint_uri(EndpointKind.PROPERTY, "created")
        )
        if type(response) is NoneType:
            return None
        return datetime.fromisoformat(cast(str, response).strip("Z"))

    async def get_current_gaze_frequency(self) -> JSONObject:
        return await self._connection.require_get(
            self.generate_endpoint_uri(EndpointKind.PROPERTY, "current-gaze-frequency")
        )

    async def get_duration(self) -> JSONObject:
        return await self._connection.require_get(
            self.generate_endpoint_uri(EndpointKind.PROPERTY, "duration")
        )

    async def get_folder(self) -> JSONObject:
        return await self._connection.require_get(
            self.generate_endpoint_uri(EndpointKind.PROPERTY, "folder")
        )

    async def set_folder(self, value: str) -> bool:
        return cast(
            bool,
            await self._connection.require_post(
                self.generate_endpoint_uri(EndpointKind.PROPERTY, "folder"), body=value
            ),
        )

    async def get_gaze_overlay(self) -> JSONObject:
        return await self._connection.require_get(
            self.generate_endpoint_uri(EndpointKind.PROPERTY, "gaze-overlay")
        )

    async def get_gaze_samples(self) -> JSONObject:
        return await self._connection.require_get(
            self.generate_endpoint_uri(EndpointKind.PROPERTY, "gaze-samples")
        )

    async def get_name(self) -> JSONObject:
        return await self._connection.require_get(
            self.generate_endpoint_uri(EndpointKind.PROPERTY, "name")
        )

    async def get_remaining_time(self) -> JSONObject:
        return await self._connection.require_get(
            self.generate_endpoint_uri(EndpointKind.PROPERTY, "remaining-time")
        )

    async def get_timezone(self) -> JSONObject:
        return await self._connection.require_get(
            self.generate_endpoint_uri(EndpointKind.PROPERTY, "timezone")
        )

    async def get_uuid(self) -> JSONObject:
        return await self._connection.require_get(
            self.generate_endpoint_uri(EndpointKind.PROPERTY, "uuid")
        )

    async def get_valid_gaze_samples(self) -> JSONObject:
        return await self._connection.require_get(
            self.generate_endpoint_uri(EndpointKind.PROPERTY, "valid-gaze-samples")
        )

    async def get_visible_name(self) -> JSONObject:
        return await self._connection.require_get(
            self.generate_endpoint_uri(EndpointKind.PROPERTY, "visible-name")
        )

    async def set_visible_name(self, value: str) -> bool:
        return cast(
            bool,
            await self._connection.require_post(
                self.generate_endpoint_uri(EndpointKind.PROPERTY, "visible-name"),
                body=value,
            ),
        )

    async def cancel(self):
        await self._connection.require_post(
            self.generate_endpoint_uri(EndpointKind.ACTION, "cancel")
        )

    async def meta_insert(self, key: str, meta: Optional[str]) -> bool:
        return cast(
            bool,
            await self._connection.require_post(
                self.generate_endpoint_uri(EndpointKind.ACTION, "meta-insert"),
                body=[key, meta],
            ),
        )

    async def meta_keys(self) -> List[str]:
        return cast(
            List[str],
            await self._connection.require_post(
                self.generate_endpoint_uri(EndpointKind.ACTION, "meta-keys")
            ),
        )

    async def meta_lookup(self, key: str) -> Optional[str]:
        return cast(
            Optional[str],
            await self._connection.require_post(
                self.generate_endpoint_uri(EndpointKind.ACTION, "meta-lookup"),
                body=[key],
            ),
        )

    async def send_event(self, tag: str, object: JSONObject) -> bool:
        return cast(
            bool,
            await self._connection.require_post(
                self.generate_endpoint_uri(EndpointKind.ACTION, "send-event"),
                body=[tag, object],
            ),
        )

    async def snapshot(self) -> bool:
        return cast(
            bool,
            await self._connection.require_post(
                self.generate_endpoint_uri(EndpointKind.ACTION, "snapshot")
            ),
        )

    async def start(self) -> bool:
        return cast(
            bool,
            await self._connection.require_post(
                self.generate_endpoint_uri(EndpointKind.ACTION, "start")
            ),
        )

    async def stop(self) -> bool:
        return cast(
            bool,
            await self._connection.require_post(
                self.generate_endpoint_uri(EndpointKind.ACTION, "stop")
            ),
        )

    async def subscribe_to_started(
        self,
    ) -> Tuple[asyncio.Queue[SignalBody], Awaitable[None]]:
        return await self._connection.subscribe_to_signal(
            self.generate_endpoint_uri(EndpointKind.SIGNAL, "started")
        )

    async def subscribe_to_stopped(
        self,
    ) -> Tuple[asyncio.Queue[SignalBody], Awaitable[None]]:
        return await self._connection.subscribe_to_signal(
            self.generate_endpoint_uri(EndpointKind.SIGNAL, "stopped")
        )
