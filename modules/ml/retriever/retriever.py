import logging

import numpy as np

from modules.ml.document_store.faiss import FAISSDocumentStore
from modules.ml.vectorizer.base import DocVectorizerBase

logger = logging.getLogger(__name__)


class Retriever:
    def __init__(
        self,
        document_store: FAISSDocumentStore = None,
        candidate_vectorizer: DocVectorizerBase = None,
        retriever_vectorizer: DocVectorizerBase = None,
    ):
        """Init an instance of a Retriever

        Args:
            document_store (FAISSDocumentStore): An instance of DocumentStore (FAISSDocumentStore) to where data is indexed and stored. Defaults to None.
            candidate_vectorizer (DocVectorizerBase): An instance of vectorizer to convert QUERY documents to embedding. Defaults to None.
            retriever_vectorizer (DocVectorizerBase): An instance of vectorizer to convert CANDIDATE documents to embeddings. Defaults to None.
        """

        self.document_store = document_store
        self.candidate_vectorizer = candidate_vectorizer
        self.retriever_vectorizer = retriever_vectorizer

    def train_candidate_vectorizer(self, training_documents=None, save_path=None):
        """
        Vectorize the document and transform into dense

        Add the vector into the index

        Not sure the output for this one because it does not link or return anything
        """

        if not training_documents or len(training_documents):
            self.training_documents = [
                document.text for document in self.document_store.get_all_documents()
            ]

            if not self.training_documents or len(self.training_documents) == 0:
                logger.warning("Fit method called with empty DocumentStore")
                return
        self.spare_documnet_embedding = self.candidate_vectorizer.fit_transform(
            self.training_documents
        )

        if save_path:
            self.candidate_vectorizer.save(save_path)

    def train_retriever_vectorizer(self, training_documents=None, save_path=None):
        """[summary]

        Args:
            training_documents ([type], optional): [description]. Defaults to None.
            save_path ([type], optional): [description]. Defaults to None.
        """
        if not training_documents or len(training_documents):
            self.training_documents = [
                document.text for document in self.document_store.get_all_documents()
            ]

            if not self.training_documents or len(self.training_documents) == 0:
                logger.warning("Fit method called with empty DocumentStore")
                return
        self.spare_documnet_embedding = self.retriever_vectorizer.fit_transform(
            self.training_documents
        )

        if save_path:
            self.retriever_vectorizer.save(save_path)

    def update_embeddings(self):
        """Update embedding of document in 1st phase to `document_store`."""

        self.document_store.update_embeddings(self.candidate_vectorizer)

    def get_candidates(
        self, query_docs: str, top_k: int = 10, index: str = None, filters=None
    ):
        """Scan through query_docs and convert it into embedding vector for comparison

        Args:
            :param query_docs: The query documents
            :param top_k: How many document to return

        Returns:
            Return a small a number of documents (top_k) that are most relevant to each query_doc
        """

        query_embs = self.candidate_vectorizer.transform(query_docs)
        score_matrix, vector_id_matrix = self.document_store.query_ids_by_embedding(
            query_emb=query_embs, filters=filters, top_k=top_k, index=index
        )

        return score_matrix, vector_id_matrix

    def _calc_scores_for_candidates(self, query_doc, candidate_ids):
        """[summary]

        Args:
            query_doc ([type]): [description]
            candidate_ids ([type]): [description]

        Returns:
            [type]: [description]
        """

        query_emb = self.retriever_vectorizer.transform([query_doc])
        candidate_ids = list(map(str, candidate_ids))

        candidate_docs = self.document_store.get_documents_by_vector_ids(candidate_ids)
        candidate_text_docs = [candidate_doc.text for candidate_doc in candidate_docs]
        candidate_embs = self.retriever_vectorizer.transform(candidate_text_docs)

        scores = candidate_embs.dot(query_emb.T)
        idx_scores = [(idx, score) for idx, score in enumerate(scores)]

        highest_score = sorted(idx_scores, key=(lambda tup: tup[1]), reverse=True)[0]

        return candidate_text_docs[highest_score[0]], highest_score[1]

    def retrieve(self, query_docs, top_k_candidates=10, index=None, filters=None):
        """[summary]

        Args:
            query_docs ([type]): [description]
            top_k_candidates ([type]): [description]
            index ([type]): [description]
            filters ([type]): [description]
        """

        _, candidate_id_matrix = self.get_candidates(
            query_docs=query_docs, top_k=top_k_candidates, index=index, filters=filters
        )

        retrieve_results = {}

        for idx, query_doc in enumerate(query_docs):
            candidate_ids = [
                candidate_id
                for candidate_id in candidate_id_matrix[idx]
                if candidate_id >= 0
            ]
            retrieve_result, score = self._calc_scores_for_candidates(
                query_doc=query_doc, candidate_ids=candidate_ids
            )
            retrieve_results[query_doc] = {
                "retrieve_result": retrieve_result,
                "similarity_score": round(score[0], 5),
            }

        return retrieve_results
