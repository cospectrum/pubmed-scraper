import pytest
import pytest_asyncio
import requests
import aiohttp


@pytest.fixture(scope='module')
def requests_session():
    return requests.session()


@pytest_asyncio.fixture
async def aiohttp_session():
    async with aiohttp.ClientSession() as session:
        yield session
