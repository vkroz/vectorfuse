"""Abstract base class defining the backend interface contract.

Every vector DB backend must implement this interface. This is the core
abstraction that allows applications to be backend-agnostic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from vectorfuse.models import (
    CollectionInfo,
    CollectionSchema,
    DeleteResult,
    GetResult,
    HybridSearchRequest,
    IndexConfig,
    IndexInfo,
    SearchRequest,
    SearchResult,
    UpsertRequest,
    UpsertResult,
)


class Backend(ABC):
    """Abstract backend interface for vector database operations.

    Implementations must handle connection lifecycle and translate
    vectorfuse models into backend-specific API calls.
    """

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    @abstractmethod
    def connect(self, **kwargs: Any) -> None:
        """Establish connection to the backend."""

    @abstractmethod
    def disconnect(self) -> None:
        """Close the backend connection and release resources."""

    @abstractmethod
    def is_connected(self) -> bool:
        """Check if the backend connection is active."""

    # ------------------------------------------------------------------
    # Collections
    # ------------------------------------------------------------------

    @abstractmethod
    def create_collection(self, name: str, schema: CollectionSchema) -> CollectionInfo:
        """Create a new collection.

        Raises:
            CollectionAlreadyExistsError: If collection already exists.
        """

    @abstractmethod
    def drop_collection(self, name: str) -> None:
        """Drop a collection and all its data.

        Raises:
            CollectionNotFoundError: If collection does not exist.
        """

    @abstractmethod
    def has_collection(self, name: str) -> bool:
        """Check if a collection exists."""

    @abstractmethod
    def list_collections(self) -> list[str]:
        """List all collection names."""

    @abstractmethod
    def describe_collection(self, name: str) -> CollectionInfo:
        """Get detailed information about a collection.

        Raises:
            CollectionNotFoundError: If collection does not exist.
        """

    # ------------------------------------------------------------------
    # Index management
    # ------------------------------------------------------------------

    @abstractmethod
    def create_index(self, collection: str, config: IndexConfig) -> None:
        """Create an index on the vector field of a collection.

        Raises:
            CollectionNotFoundError: If collection does not exist.
        """

    @abstractmethod
    def drop_index(self, collection: str) -> None:
        """Drop the index from a collection's vector field.

        Raises:
            CollectionNotFoundError: If collection does not exist.
        """

    @abstractmethod
    def describe_index(self, collection: str) -> IndexInfo | None:
        """Describe the index on a collection's vector field.

        Returns None if no index exists.
        """

    # ------------------------------------------------------------------
    # Vector CRUD
    # ------------------------------------------------------------------

    @abstractmethod
    def upsert(self, collection: str, request: UpsertRequest) -> UpsertResult:
        """Insert or update vectors in a collection.

        Raises:
            CollectionNotFoundError: If collection does not exist.
            DimensionMismatchError: If vector dimensions don't match schema.
        """

    @abstractmethod
    def get(self, collection: str, ids: list[str], include_vectors: bool = False) -> GetResult:
        """Retrieve vectors by their IDs.

        Raises:
            CollectionNotFoundError: If collection does not exist.
        """

    @abstractmethod
    def delete(self, collection: str, ids: list[str]) -> DeleteResult:
        """Delete vectors by their IDs.

        Raises:
            CollectionNotFoundError: If collection does not exist.
        """

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    @abstractmethod
    def search(self, collection: str, request: SearchRequest) -> SearchResult:
        """Perform similarity search.

        Raises:
            CollectionNotFoundError: If collection does not exist.
        """

    @abstractmethod
    def hybrid_search(self, collection: str, request: HybridSearchRequest) -> SearchResult:
        """Perform hybrid (dense + sparse) search.

        Raises:
            CollectionNotFoundError: If collection does not exist.
            NotImplementedError: If the backend does not support hybrid search.
        """
