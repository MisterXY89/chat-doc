import json
import os
import pickle

import docx
import pretty_errors


class DocXReader(object):
    def __init__(self, config, logger) -> None:
        self.config = config
        self.logger = logger

    def _extract_paragraph(self, paragraph):
        return {
            "text": paragraph.text,
            "style": paragraph.style.name,
        }

    def _extract_section(self, section):
        section_data = {"section": []}
        for paragraph in section.paragraphs:
            section_data["section"].append(self._extract_paragraph(paragraph))
        return section_data

    def read_text(self, fn, output_format="dict"):
        print(os.getcwd())
        doc = docx.Document(fn)

        doc_data = {"document": []}
        for section in doc.sections:
            doc_data["document"].append(self._extract_section(section))

        if output_format == "json":
            return json.dumps(doc_data, indent=2)
        elif output_format == "dict":
            return doc_data

        # self.logger.warning(f"Output format {output_format}') not supported - must be one of json or dict")
        return None

    def parse_content(string):
        return string

    def save_cotent(self, content, fn="ICD-doc-content.pkl"):
        with open(fn, "wb") as fi:
            pickle.dump(content, fi)

    def read_content(self, fn):
        try:
            with open(fn, "rb") as fi:
                content = pickle.load(fi)

        except Exception as e:
            content = None
            # self.logger.error(e)
            print(e)
        return content

    def read(self, fn, save=True, force_parse=False):
        text_content = self.read_text(fn)
        content = self.parse_content(text_content)

        if save:
            self.save_cotent(content)

        return content


if __name__ == "__main__":
    path = "/Users/tilmankerl/Documents/UNI/03_WS23/Applied Deep Learning/project/data/print_ICD11_Primary_Care_Low_RS-en.docx"
    reader = DocXReader(None, None)
    data = reader.read(path)
    print(data)
