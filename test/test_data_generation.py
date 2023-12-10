import os
import sys

import pytest


def _test_build(name):
    from chat_doc.dataset_generation.dataset_factory import DatasetFactory

    dataset_factory = DatasetFactory()
    dataset_factory.build_dataset(name=name)

    assert dataset_factory.dataset is not None
    assert os.path.exists(f"data/prompt_{name.upper()}.pkl")


def test_full_build():
    from chat_doc.dataset_generation.dataset_factory import DatasetFactory

    dataset_factory = DatasetFactory()
    dataset_factory.build_dataset(name="full")

    assert dataset_factory.dataset is not None
    assert os.path.exists("data/full_prompts.pkl")


# def test_full_dialogue_build():
#     from chat_doc.dataset_generation.dataset_factory import DatasetFactory

#     dataset_factory = DatasetFactory()
#     dataset_factory.build_dataset(name="dialogue-full")

#     assert dataset_factory.dataset is not None
#     assert os.path.exists("data/full_dialogue_prompts.pkl")


def test_icd_build():
    _test_build("icd")


def test_pmc_build():
    _test_build("pmc")


def test_diagnose_me_build():
    _test_build("diagnose")


# def test_med_dialogue_build():
#     _test_build("med-dialogue")


if __name__ == "__main__":
    pytest.main()
