import os
import pickle
import sqlite3
import urllib.request
from pathlib import Path

import jsonpickle
from tqdm.auto import tqdm

from modules.ml.document_store.faiss import FAISSDocumentStore
from modules.ml.preprocessor.vi_preprocessor import ViPreProcessor


def data_prep(data_dict):
    """
    To transform data provided by DocBao to fit with the schema at FAISSDocumentStore
    """

    content = list()
    for c in data_dict["content"]:
        if (c["type"] == "text") & (len(c["content"].split(" ")) > 10):
            content.append(c["content"])
    content = " ".join(content)

    meta = dict()
    for k in data_dict.keys():
        if k != "content":
            meta[k] = data_dict[k]

    return content, meta


def main():

    cwd = Path(__file__).parent
    if not os.path.exists(os.path.join(cwd, "post_dataset.pkl")):
        print("Downloading sample data of TopDup")
        urllib.request.urlretrieve(
            "https://storage.googleapis.com/topdup/dataset/post_dataset.pkl",
            os.path.join(cwd, "post_dataset.pkl"),
        )

    print("Preprocessing documents")
    processor = ViPreProcessor()
    data = pickle.load(open(os.path.join(cwd, "post_dataset.pkl"), "rb"))
    docs = list()
    for d in tqdm(data[:1000]):
        content, meta = data_prep(jsonpickle.loads(d))
        doc = processor.clean({"text": content})
        for m in meta.keys():
            if isinstance(meta[m], list):  # serialize list
                meta[m] = "|".join(meta[m])
        doc["meta"] = meta
        docs.append(doc)

    print("Ingesting data to SQLite database")
    db_path = os.path.join(cwd, "topdup.db")
    if os.path.exists(db_path):
        os.remove(db_path)
    with sqlite3.connect(db_path):
        document_store = FAISSDocumentStore(sql_url=f"sqlite:///{db_path}")
        document_store.write_documents(docs)

    pass


if __name__ == "__main__":
    main()
