import os
from pathlib import Path

# import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modules.ml.document_store.faiss import FAISSDocumentStore
from modules.ml.document_store.sql import DocumentORM, ORMBase
from modules.ml.retriever.retriever import Retriever
from modules.ml.vectorizer.tf_idf import TfidfDocVectorizer

parent_cwd = Path(__file__).parent.parent
test_db_path = os.path.join(parent_cwd, "document_store/topdup.db")


def test_retriever_with_database():

    print("Init vectorizers")
    cand_vectorizer = TfidfDocVectorizer(128)
    rtrv_vectorizer = TfidfDocVectorizer(256)

    print("Init DocumentStore")
    document_store = FAISSDocumentStore(sql_url=f"sqlite:///{test_db_path}")

    print("Init retriever")
    retriever = Retriever(
        document_store=document_store,
        candidate_vectorizer=cand_vectorizer,
        retriever_vectorizer=rtrv_vectorizer,
    )

    # Train vectorizers for two phases of searching
    print("Training vectorizers")
    retriever.train_candidate_vectorizer()
    retriever.train_retriever_vectorizer()

    # Update trained embeddings to DocumentStore
    print("Updating embeddings to DocumentStore")
    retriever.update_embeddings()

    # Get a document from the database as input for retriever
    print("Query sample input from database")
    url = f"sqlite:///{test_db_path}"
    engine = create_engine(url)
    ORMBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(DocumentORM).filter_by().limit(5)

    # Get text from query to input
    input_doc = query.all()[0].text
    print(" ".join(input_doc.split(" ")[:50]))  # print the query doc

    # Init expected result
    expected_text_result = input_doc
    expected_score_result = 1

    print("Retrieving")

    result = retriever.retrieve([input_doc], top_k_candidates=10)
    print(
        " ".join(result[input_doc]["retrieve_result"].split(" ")[:50])
    )  # print the retrieved doc
    assert result[input_doc]["retrieve_result"] == expected_text_result
    assert result[input_doc]["similarity_score"] == expected_score_result


if __name__ == "__main__":
    test_retriever_with_database()
