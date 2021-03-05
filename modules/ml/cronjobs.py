import logging
import os
from datetime import datetime, timedelta

import schedule

from modules.ml.retriever.retriever import Retriever
from modules.ml.utils import get_local_connection, get_remote_connection
from modules.ml.vectorizer.tf_idf import TfidfDocVectorizer

# TODO: config remote logging

DB_PATH = os.getenv('LOCAL_DB_PATH', 'local.db')
POSTGRES_URL = os.getenv('POSTGRES_URI', 'localhost:5432')
CAND_DIM = 768
RTRV_DIM = 1024
CAND_PATH = os.getenv('CAND_PATH', 'cand.bin')
RTRV_PATH = os.getenv('RTRV_PATH', 'rtrv.bin')
IDX_PATH = os.getenv('IDX_PATH', 'index.bin')


local_doc_store = get_local_connection(DB_PATH)
remote_doc_store = get_remote_connection(POSTGRES_URL)


def update_local_db():
    """
    Write a proper docstring later
    This method runs in serial as sfollow:
    1. Get document ids from remote and local db
    2. Check if there is new document
    If Yes:
    3. Write new document to local db
    4. Update embeddings on small FAISS index
    5. Update vector ids on local db
    6. Run sequential retriever to pre-calculate the similarity scores
    and update on local db meta data
    """
    # TODO: implement this

    if not local_doc_store or not remote_doc_store:  # noqa
        logging.warning('DB connection not initialized, trying re-connect...')
        local_doc_store = get_local_connection(DB_PATH)
        remote_doc_store = get_remote_connection(POSTGRES_URL)
        if not local_doc_store or not remote_doc_store:
            logging.error('DB initialization failed, quit local_update...')
            return

    new_ids = remote_doc_store.get_document_ids(from_time=datetime.now() - timedelta(minutes=1))  # noqa
    if not new_ids:
        logging.info(f'No new updates in local db at {datetime.now()}')
        return

    local_ids = local_doc_store.get_document_ids()

    # filter existing ids in local out of recent updated ids from remote db

    new_ids = [_id for _id in new_ids if _id not in local_ids]

    docs = remote_doc_store.get_document_by_id(new_ids)
    logging.info(f'Retrieved {len(docs)} at {datetime.now()}')

    local_doc_store.write_documents(docs)
    logging.info('Stored documents to local db')

    if not os.path.exists(CAND_PATH) or not os.path.exists(RTRV_PATH):
        logging.critical('Vectorizer models not found, quiting job...')
        return

    local_retriever = Retriever(
        document_store=local_doc_store,
        candidate_vectorizer=TfidfDocVectorizer(CAND_DIM),
        retriever_vectorizer=TfidfDocVectorizer(RTRV_DIM)
    )
    remote_retriever = Retriever(
        document_store=remote_doc_store,
        candidate_vectorizer=TfidfDocVectorizer(CAND_DIM),
        retriever_vectorizer=TfidfDocVectorizer(RTRV_DIM)
    )

    remote_retriever.train_candidate_vectorizer(
        retrain=False, save_path=CAND_PATH)
    remote_retriever.train_retriever_vectorizer(
        retrain=False, save_path=RTRV_PATH)

    local_retriever.train_candidate_vectorizer(
        retrain=False, save_path=CAND_PATH)
    local_retriever.train_retriever_vectorizer(
        retrain=False, save_path=RTRV_PATH)
    logging.info('Vectorizers loaded')

    reindex = os.path.exists(IDX_PATH)
    local_retriever.update_embeddings(
        retrain=reindex, save_path=IDX_PATH, sql_url=DB_PATH)
    logging.info('Embeddings updated')

    local_results = local_retriever.batch_retrieve(docs)
    remote_result = remote_retriever.batch_retrieve(docs)
    for _id, l, r in zip(new_ids, local_results, remote_result):
        local_sim = l.get('similarity_score', 0)
        remote_sim = r.get('similarity_score', 0)
        if local_sim > remote_sim:
            sim_data = {
                'sim_score': local_sim,
                'similar_to': l['retrieve_result']
            }
            remote_doc_store.update_document_meta(_id, sim_data)
    logging.info('Similarity scores updated into metadata')


def update_remote_db():
    """
    Write a proper docstring later
    This method runs in serial as follow:
    1. Update embeddings on large FAISS index
    2. Update vector ids on remote db
    3. Update meta data of documents on local db to remote db
    4. Clear local db
    """
    remote_retriever = Retriever(
        document_store=remote_doc_store,
        candidate_vectorizer=TfidfDocVectorizer(CAND_DIM),
        retriever_vectorizer=TfidfDocVectorizer(RTRV_DIM)
    )
    remote_retriever.train_candidate_vectorizer(retrain=False, save_path=CAND_PATH)
    remote_retriever.update_embeddings(retrain=True)
    logging.info('Remote embeddings and vector ids updated')

    local_doc_store.delete_all_documents()


if __name__ == '__main__':
    schedule.every().minute.do(update_local_db)
    schedule.every().day.at("00:00").do(update_remote_db)
    while True:
        schedule.run_pending()
