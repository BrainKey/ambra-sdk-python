from ambra_sdk import API_VERSION, MODELS_VERSION, STORAGE_VERSION


def test_api_version():
    assert API_VERSION == 'LBL0022 v55.0 2022-08-03'


def test_models_version():
    assert MODELS_VERSION == 'LBL0022 v55.0 2022-08-03'


def test_storage_version():
    assert STORAGE_VERSION == 'LBL0038 v23.0 2022-08-03'
