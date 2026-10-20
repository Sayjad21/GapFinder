"""A transient server error on a Sandboxes status poll is retried, not turned into a cancelled run."""

import asyncio

from contree_sdk.sdk.exceptions.api import ApiStatusCodeError, ForbiddenError

from gapfinder.sandbox import backend


class FakeApi:
    def __init__(self, fail):
        self.fail, self.calls = list(fail), 0

    async def get_operation_status(self, op):
        self.calls += 1
        if self.fail:
            raise self.fail.pop(0)
        return "done"


def _err(cls, status):
    e = cls.__new__(cls)
    e.status = status
    return e


def test_a_500_on_a_poll_is_retried(monkeypatch):
    async def no_sleep(_):
        return None

    monkeypatch.setattr(asyncio, "sleep", no_sleep)
    sdk = type("Sdk", (), {})()
    sdk._api = FakeApi([_err(ApiStatusCodeError, 500), _err(ApiStatusCodeError, 502)])
    backend._retry_status_polls(sdk)
    assert asyncio.run(sdk._api.get_operation_status("op")) == "done" and sdk._api.calls == 3
    sdk2 = type("Sdk", (), {})()
    sdk2._api = FakeApi([_err(ForbiddenError, 403)])
    backend._retry_status_polls(sdk2)
    try:
        asyncio.run(sdk2._api.get_operation_status("op"))
        raise AssertionError("a 403 must not be retried")
    except ForbiddenError:
        pass
