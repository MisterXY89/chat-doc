import logging
import os
import sys
import time

import pytest


def _delete_existing_data():
    data_dir = os.path.join(os.getcwd(), "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

        print("Created data directory")
    for file in os.listdir(data_dir):
        os.remove(os.path.join(data_dir, file))
    print("Deleted existing data")


def pytest_generate_tests(metafunc):
    os.environ["HF_TOKEN"] = "xxx"
    os.environ["FLASK_APP_SECRET"] = str(time.time())
    os.environ["WTF_CSRF_SECRET_KEY"] = str(time.time() + 2)
    os.environ["FLASK_APP_NAME"] = "Chat-Doctor"
    os.environ["FLASK_APP_DB_NAME"] = "app.db"


@pytest.fixture(autouse=True)
def run_around_tests():
    logging.disable(logging.CRITICAL)

    # os.environ.get

    # append to path to import from chat_doc
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    _delete_existing_data()

    yield

    logging.disable(logging.NOTSET)
