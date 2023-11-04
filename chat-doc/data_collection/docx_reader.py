import os
import pickle

import docx2txt

from ..config import config


def read_text(fn):
    # extract text
    text = docx2txt.process(fn)
    print(text)


def parse_content(string):
    return string


def save_cotent(content, fn="ICD-doc-content.pkl"):
    with open(fn, "wb") as fi:
        pickle.dump(content, fi)


def read_content(fn):
    try:
        with open(fn, "rb") as fi:
            content = pickle.load(fi)

    except Exception as e:
        content = None
        print(e)
    return content


def get_docx_data(fn, save=True, force_parse=False):
    if not force_parse:
        content = read_content()
        if content:
            return content

    text_content = read_text(fn)
    content = parse_content(text_content)

    if save:
        save_cotent(content)

    return content


if __name__ == "__main__":
    data = get_docx_data("../../data/print_ICD11_MMS-en.docx")
    print(data)
