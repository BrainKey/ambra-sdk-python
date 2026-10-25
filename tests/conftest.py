import asyncio
import os

import pytest
from dynaconf import settings

from ambra_sdk.api import Api, AsyncApi

_NO_CREDS_REASON = (
    'requires live Ambra API credentials: provide a secrets.toml with '
    '[testing.api] url/username/password (and do not set AMBRA_SKIP_INTEGRATION)'
)

# Root fixtures that build a live-credentialed API client. Every integration
# fixture (account, study, storage_cluster, ...) depends on one of these, so a
# test's full fixture closure contains one of these names iff it needs the API.
_CREDENTIAL_FIXTURES = frozenset({'api', 'async_api'})


def _has_credentials():
    """Whether live Ambra API credentials are configured.

    Integration tests need a real API. Without credentials (e.g. CI) they
    are skipped instead of erroring. Set ``AMBRA_SKIP_INTEGRATION`` to force
    skipping even when a secrets file is present.

    :return: True if credentials are available
    """
    if os.environ.get('AMBRA_SKIP_INTEGRATION'):
        return False
    try:
        api = settings.from_env('testing').API
        return bool(api['url'] and api['username'] and api['password'])
    except Exception:  # noqa: WPS424, B902 - dynaconf raises various errors when unset
        return False


def pytest_collection_modifyitems(config, items):
    """Skip integration tests at collection time when no credentials exist.

    Skipping here (rather than inside the fixtures) avoids ever setting up the
    live-API fixtures, which also sidesteps async-fixture machinery for the
    async integration tests. Covers tests that pull in a credential fixture and
    tests that read settings directly (marked ``requires_credentials``).

    :param config: pytest config
    :param items: collected test items
    """
    if _has_credentials():
        return
    skip_no_creds = pytest.mark.skip(reason=_NO_CREDS_REASON)
    for item in items:
        needs_creds = (
            _CREDENTIAL_FIXTURES & set(getattr(item, 'fixturenames', ()))
            or item.get_closest_marker('requires_credentials')
        )
        if needs_creds:
            item.add_marker(skip_no_creds)


@pytest.fixture(scope='session', autouse=True)
def set_test_settings():
    """Set dynaconf env for testing."""
    settings.configure(ENV_FOR_DYNACONF='testing')


@pytest.fixture(scope='module')
def api():
    """Get api.

    :yields: valid  ambra api
    """
    url = settings.API['url']
    username = settings.API['username']
    password = settings.API['password']
    api = Api.with_creds(
        url,
        username,
        password,
        'SDK testing',
    )
    yield api
    api.logout()


@pytest.fixture(scope='module')
def event_loop():
    """Event loop module scoped.

    :return: event loop for module scope
    """
    return asyncio.get_event_loop()


@pytest.fixture(scope='module')
async def async_api(event_loop):
    """Get api.

    :param event_loop: event loop for modules scope
    :yields: valid  ambra api
    """
    url = settings.API['url']
    username = settings.API['username']
    password = settings.API['password']
    api = AsyncApi.with_creds(
        url,
        username,
        password,
        'SDK testing',
    )
    yield api
    await api.logout()


pytest_plugins = [
    'tests.fixtures.account',
    'tests.fixtures.async_account',
    'tests.fixtures.study',
    'tests.fixtures.async_study',
    'tests.fixtures.ws',
    'tests.fixtures.customfield',
]


def pytest_generate_tests(metafunc):
    """Gen tests.

    :param metafunc: metafunc
    """
    if 'storage_cluster' in metafunc.fixturenames:
        cluster_names = settings \
            .from_env('testing') \
            .get('CLUSTER_STORAGE_NAMES', ['DEFAULT'])
        metafunc.parametrize(
            'storage_cluster',
            cluster_names,
            indirect=True,
        )
