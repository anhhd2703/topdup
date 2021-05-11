import os
from pathlib import Path

from modules.ml.document_store.faiss import FAISSDocumentStore
from modules.ml.retriever.retriever import Retriever
from modules.ml.vectorizer.tf_idf import TfidfDocVectorizer

parent_cwd = Path(__file__).parent.parent


def test_retriever_with_database():

    cand_dim = 768
    rtrv_dim = 1024
    sql_url = "postgresql+psycopg2://user:pwd@host/topdup_articles"

    print("Init vectorizers")
    cand_vectorizer = TfidfDocVectorizer(cand_dim)
    rtrv_vectorizer = TfidfDocVectorizer(rtrv_dim)

    print("Init DocumentStore")
    document_store = FAISSDocumentStore(
        sql_url=sql_url, vector_dim=cand_dim, index_buffer_size=5000
    )

    print("Init retriever")
    retriever = Retriever(
        document_store=document_store,
        candidate_vectorizer=cand_vectorizer,
        retriever_vectorizer=rtrv_vectorizer,
    )

    # Train vectorizers for two phases of searching
    if os.path.exists(os.path.join(parent_cwd, "cand.bin")):
        print("Loading vectorizers")
        retriever.train_candidate_vectorizer(
            retrain=False, save_path=os.path.join(parent_cwd, "cand.bin")
        )
        retriever.train_retriever_vectorizer(
            retrain=False, save_path=os.path.join(parent_cwd, "rtrv.bin")
        )
    else:
        print("Training vectorizers")
        retriever.train_candidate_vectorizer(
            retrain=True, save_path=os.path.join(parent_cwd, "cand.bin")
        )
        retriever.train_retriever_vectorizer(
            retrain=True, save_path=os.path.join(parent_cwd, "rtrv.bin")
        )

    # Update trained embeddings to index of FAISSDocumentStore
    if os.path.exists(os.path.join(parent_cwd, "index.bin")):
        print("Loading index of FAISSDocumentStore")
        retriever.update_embeddings(
            retrain=False,
            save_path=os.path.join(parent_cwd, "index.bin"),
            sql_url=sql_url,
        )
    else:
        print("Updating embeddings to index of FAISSDocumentStore")
        retriever.update_embeddings(
            retrain=True,
            save_path=os.path.join(parent_cwd, "index.bin"),
            sql_url=sql_url,
        )

    # Get a pair of duplicated articles from topdup.xyz to test
    input_doc = document_store.get_document_by_id(
        id="76a0874a-b0db-477c-a0ca-9e65b8ccf2f3"
    ).text
    print(" ".join(input_doc.split(" ")[:50]))  # print the query doc

    print("Retrieving")
    result = retriever.batch_retrieve([input_doc], top_k_candidates=10)
    print(
        " ".join(result[0]["retrieve_result"].split(" ")[:50])
    )  # print the retrieved doc


if __name__ == "__main__":
    test_retriever_with_database()
