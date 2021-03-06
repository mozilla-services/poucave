import time

from aioresponses import CallbackResult

from checks.core.latency import run


async def test_positive(mock_aioresponses):
    def callback(url, **kwargs):
        time.sleep(0.100)
        return CallbackResult(status=200)

    url = "http://server.local/__heartbeat__"
    mock_aioresponses.get(url, callback=callback)

    status, data = await run(url, max_milliseconds=200)

    assert status is True
    assert 100 <= data < 200


async def test_negative(mock_aioresponses):
    def callback(url, **kwargs):
        time.sleep(0.100)
        return CallbackResult(status=200)

    url = "http://server.local/__heartbeat__"
    mock_aioresponses.get(url, callback=callback)

    # Since Python 3.5, time.sleep() is guaranteed to
    # sleep at least for the time given.
    status, data = await run(url, max_milliseconds=100)

    assert status is False
    assert data >= 100


async def test_unreachable(mock_aioresponses):
    status, data = await run("http://not-mocked", max_milliseconds=100)

    assert status is False
    assert data == "Connection refused: GET http://not-mocked"
