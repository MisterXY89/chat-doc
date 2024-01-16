import pandas as pd


def parse_data():
    _df = pd.read_json("chat_doc/data/pinglab-ICD11-data.json")
    _df = _df.query("definition != 'Key Not found'")
    _df.reset_index(inplace=True)

    _df = _df[["name", "definition", "id"]]
    # _df["text"] = "Name:" + _df["name"] + "\nDefinition: " + _df["definition"]

    return _df


def store_data(df):
    # store data in db or csv?
    df.to_csv("chat_doc/data/icd11.csv", index=False)


def main():
    df = parse_data()
    store_data(df)


if __name__ == "__main__":
    main()
