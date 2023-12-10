import logging
import os
import sys

import pytest


def _delete_existing_data():
    data_dir = os.path.join(os.getcwd(), "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

        print("Created data directory")
    for file in os.listdir(data_dir):
        os.remove(os.path.join(data_dir, file))
    print("Deleted existing data")


@pytest.fixture(autouse=True)
def run_around_tests():
    logging.disable(logging.CRITICAL)

    # rename .env.example to .env before running tests
    os.rename(".env.example", ".env")

    # append to path to import from chat_doc
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    _delete_existing_data()

    yield

    logging.disable(logging.NOTSET)
