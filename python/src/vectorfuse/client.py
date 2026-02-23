"""VectorFuse client — the main entry point for all vector operations."""

from __future__ import annotations

from typing import Any

from vectorfuse.backends import get_backend
from vectorfuse.backends.base import Backend
from vectorfuse.models import (
    CollectionInfo,
    CollectionSchema,
    DeleteResult,
    DistanceMetric,
    GetResult,
    HybridSearchRequest,
    IndexConfig,
    IndexInfo,
    IndexType,
    SearchMatch,
    SearchRequest,
    SearchResult,
    UpsertRequest,
    UpsertResult,
)


class VectorFuse:
    """Unified vector database client.

    Args:
        backend: Name of the backend (e.g., "milvus", "zilliz").
        **kwargs: Connection parameters forwarded to the backend's connect() method.

    Example::

        mux = VectorFuse(backend="milvus", uri="http://localhost:19530")
        mux.create_collection("docs", dimension=768)
        mux.upsert("docs", ids=["d1"], vectors=[[0.1] * 768])
        results = mux.search("docs", query_vector=[0.1] * 768, top_k=5)
        mux.close()
    """

    def __init__(self, backend: str, **kwargs: Any) -> None:
        self._backend_name = backend
        self._backend: Backend = get_backend(backend)
        self._backend.connect(**kwargs)

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> VectorFuse:
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    def close(self) -> None:
        """Close the backend connection."""
        self._backend.disconnect()

    @property
    def is_connected(self) -> bool:
        return self._backend.is_connected()

    # ------------------------------------------------------------------
    # Collections
    # ------------------------------------------------------------------

    def create_collection(
        self,
        name: str,
        dimension: int,
        metric: DistanceMetric = DistanceMetric.COSINE,
        description: str = "",
    ) -> CollectionInfo:
        """Create a new vector collection."""
        schema = CollectionSchema(dimension=dimension, metric=metric, description=description)
        return self._backend.create_collection(name, schema)

    def drop_collection(self, name: str) -> None:
        """Drop a collection and all its data."""
        self._backend.drop_collection(name)

    def has_collection(self, name: str) -> bool:
        """Check if a collection exists."""
        return self._backend.has_collection(name)

    def list_collections(self) -> list[str]:
        """List all collections."""
        return self._backend.list_collections()

    def describe_collection(self, name: str) -> CollectionInfo:
        """Get collection info."""
        return self._backend.describe_collection(name)

    # ------------------------------------------------------------------
    # Index management
    # ------------------------------------------------------------------

    def create_index(
        self,
        collection: str,
        index_type: IndexType = IndexType.AUTOINDEX,
        metric: DistanceMetric = DistanceMetric.COSINE,
        **params: Any,
    ) -> None:
        """Create an index on the collection's vector field."""
        config = IndexConfig(index_type=index_type, metric=metric, params=params)
        self._backend.create_index(collection, config)

    def drop_index(self, collection: str) -> None:
        """Drop the index from a collection."""
        self._backend.drop_index(collection)

    def describe_index(self, collection: str) -> IndexInfo | None:
        """Describe the index on a collection. Returns None if no index."""
        return self._backend.describe_index(collection)

    # ------------------------------------------------------------------
    # Vector CRUD
    # ------------------------------------------------------------------

    def upsert(
        self,
        collection: str,
        ids: list[str],
        vectors: list[list[float]],
        metadata: list[dict[str, Any]] | None = None,
    ) -> UpsertResult:
        """Insert or update vectors."""
        request = UpsertRequest(ids=ids, vectors=vectors, metadata=metadata)
        return self._backend.upsert(collection, request)

    def get(
        self,
        collection: str,
        ids: list[str],
        include_vectors: bool = False,
    ) -> GetResult:
        """Retrieve vectors by ID."""
        return self._backend.get(collection, ids, include_vectors=include_vectors)

    def delete(self, collection: str, ids: list[str]) -> DeleteResult:
        """Delete vectors by ID."""
        return self._backend.delete(collection, ids)

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(
        self,
        collection: str,
        query_vector: list[float],
        top_k: int = 10,
        filter: dict[str, Any] | None = None,
        include_vectors: bool = False,
        include_metadata: bool = True,
        **params: Any,
    ) -> SearchResult:
        """Perform similarity search."""
        request = SearchRequest(
            query_vector=query_vector,
            top_k=top_k,
            filter=filter,
            include_vectors=include_vectors,
            include_metadata=include_metadata,
            params=params,
        )
        return self._backend.search(collection, request)

    def hybrid_search(
        self,
        collection: str,
        dense_vector: list[float],
        sparse_vector: dict[int, float] | None = None,
        top_k: int = 10,
        alpha: float = 0.5,
        filter: dict[str, Any] | None = None,
        include_vectors: bool = False,
        include_metadata: bool = True,
        **params: Any,
    ) -> SearchResult:
        """Perform hybrid (dense + sparse) search."""
        request = HybridSearchRequest(
            dense_vector=dense_vector,
            sparse_vector=sparse_vector,
            top_k=top_k,
            alpha=alpha,
            filter=filter,
            include_vectors=include_vectors,
            include_metadata=include_metadata,
            params=params,
        )
        return self._backend.hybrid_search(collection, request)
