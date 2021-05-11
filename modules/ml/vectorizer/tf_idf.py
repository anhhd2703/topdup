import pickle
from typing import List

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from modules.ml.schema import Document
from modules.ml.vectorizer.base import DocVectorizerBase


class TfidfDocVectorizer(DocVectorizerBase):
    def __init__(self, vector_dim: int = 128, **kwargs):
        """
        Vectorize the documents and return a vector that has been embedding
        for indexer or comparison.

        Args:
            vector_dim (int): Number dimentions of embedding vectors for 1st phase.
                Defaults to 128.
            **kwargs: Arbitrary keyword arguments.
        """

        # Init vectorizer
        self.vectorizer = TfidfVectorizer(max_features=vector_dim, **kwargs)
        # Set is_trained = True if vectorizer is trained, is_trained = False
        self.is_trained = False
        self.vector_dim = vector_dim

    def fit(self, train_documents: list = None) -> TfidfVectorizer:
        """Fit `train_documents` into the tf-idf and return tfidf vectorizer.

        Args:
            train_documents (list): List of training documents for vectorizer.
                Defaults to None.

        Returns:
            Tf-IDF vectorizers trained from given docs.
        """

        vectorizer = self.vectorizer.fit(train_documents)
        self.is_trained = True

        return vectorizer

    def fit_transform(self, train_documents: list = None):
        """Learn vocabulary and idf, return embedding matrix of training documents.
            This is equivalent to fit followed by transform,
            but more efficiently implemented.

        Args:
            train_documents (list): List of training documents for vectorizer. Defaults to None.

        Returns:
            np.array: Embedding matrix of training documents.
        """

        transform_vector = np.array(
            self.vectorizer.fit_transform(train_documents).todense()
        )
        self.is_trained = True

        return transform_vector

    def transform(self, documents: list = None):
        """Transform `documents` into the tf-idf vectorizer and return
        a list of vector and convert to dense.

        Args:
            documents (list): List of documents to vectorize.

        Returns:
            np.array: Embedding matrix of input documents.
        """

        # Transform `documents` into the tf-idf vectorizer and return a list of vector and convert to dense.
        transform_vectors = np.array(self.vectorizer.transform(documents).todense())

        return transform_vectors

    def transform_document_objects(self, documents: List[Document]) -> np.ndarray:
        """
        Transform given list of Document object

        Args:
            documents (List[Document])

        Returns:
            np.ndarray: Embeddings
        """

        document_text = [document.text for document in documents]

        return self.transform(document_text)

    def save(self, tfidf_vectorizer_path):
        """Save tf_idf model to the pickle file.

        Args:
            model_path (str): Path to save to.
        """
        with open(tfidf_vectorizer_path, "wb") as fw:
            pickle.dump(self, fw)

    @classmethod
    def load(cls, model_path):
        """Load vectorizer object from a pickle file.

        Args:
            model_path (str): Path to tf_idf model.

        Returns:
            TfidfDocVectorizer: A vectorizer which is loaded.
        """

        # with open(model_path, "rb") as f:
        #     tfidf_vectorizer = pickle.load(f)
        tfidf_vectorizer = pickle.load(open(model_path, "rb"))

        return tfidf_vectorizer
