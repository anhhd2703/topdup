import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union

from modules.ml.schema import Document

logger = logging.getLogger(__name__)


class BaseDocumentStore(ABC):
    """
    Base class for implementing DocumentStores.
    """

    index: Optional[str]
    label_index: Optional[str]
    similarity: Optional[str]

    @abstractmethod
    def write_documents(
        self, documents: Union[List[dict], List[Document]], index: Optional[str] = None
    ):
        pass

    @abstractmethod
    def get_all_documents(
        self,
        index: Optional[str] = None,
        filters: Optional[Dict[str, List[str]]] = None,
        return_embedding: Optional[bool] = None,
    ) -> List[Document]:
        pass

    @abstractmethod
    def get_document_by_id(
        self, id: str, index: Optional[str] = None
    ) -> Optional[Document]:
        pass

    @abstractmethod
    def get_document_count(
        self,
        filters: Optional[Dict[str, List[str]]] = None,
        index: Optional[str] = None,
    ) -> int:
        pass

    @abstractmethod
    def query_by_embedding(
        self,
        query_emb: List[float],
        filters: Optional[Optional[Dict[str, List[str]]]] = None,
        top_k: int = 10,
        index: Optional[str] = None,
        return_embedding: Optional[bool] = None,
    ) -> List[Document]:
        pass

    @abstractmethod
    def delete_all_documents(
        self, index: str, filters: Optional[Dict[str, List[str]]] = None
    ):
        pass
