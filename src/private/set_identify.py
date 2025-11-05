class Mobile:
    def __init__(self) -> None:
        self.payload = None
        self.data = None  # Will be set after payload is built
        self.device_type = None

    async def identify(self) -> str:
        """Override the identify method to use mobile properties."""
        self.device_type = "Discord iOS"

        self.payload = {
            'op': self.IDENTIFY,
            'd': {
                'token': self.token,
                'properties': {
                    '$os': '',
                    '$browser': self.device_type,
                    '$device': self.device_type,
                    '$referrer': '',
                    '$referring_domain': ''
                },
                'compress': True,
                'large_threshold': 250,
                'v': 3
            }
        }

        self.data = self.payload["d"]
        if self.shard_id is not None and self.shard_count is not None:
            self.data["shard"] = [self.shard_id, self.shard_count]

        state = self._connection
        if state._activity is not None or state._status is not None:
            self.data["presence"] = {
                "status": state._status,
                "game": state._activity,
                "since": 0,
                "afk": False,
            }

        if state._intents is not None:
            self.data["intents"] = state._intents.value

        await self.call_hooks("before_identify", self.shard_id, initial=self._initial_identify)
        await self.send_as_json(self.payload)

class PC:
    def __init__(self) -> None:
        self.payload = None
        self.data = None  # Will be set after payload is built
        self.device_type = None

    async def identify(self) -> str:
        """Override the identify method to use PC properties."""
        self.device_type = "Discord Client"

        self.payload = {
            'op': self.IDENTIFY,
            'd': {
                'token': self.token,
                'properties': {
                    '$os': '',
                    '$browser': self.device_type,
                    '$device': self.device_type,
                    '$referrer': '',
                    '$referring_domain': ''
                },
                'compress': True,
                'large_threshold': 250,
                'v': 3
            }
        }

        self.data = self.payload["d"]
        if self.shard_id is not None and self.shard_count is not None:
            self.data["shard"] = [self.shard_id, self.shard_count]

        state = self._connection
        if state._activity is not None or state._status is not None:
            self.data["presence"] = {
                "status": state._status,
                "game": state._activity,
                "since": 0,
                "afk": False,
            }

        if state._intents is not None:
            self.data["intents"] = state._intents.value

        await self.call_hooks("before_identify", self.shard_id, initial=self._initial_identify)
        await self.send_as_json(self.payload)