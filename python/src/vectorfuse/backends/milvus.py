"""Milvus/Zilliz backend implementation.

Requires: pip install vectorfuse[milvus]
"""

from __future__ import annotations

from typing import Any

from vectorfuse.backends.base import Backend
from vectorfuse.exceptions import BackendError
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

try:
    from pymilvus import MilvusClient
except ImportError:
    MilvusClient = None  # type: ignore[assignment, misc]


class MilvusBackend(Backend):
    """Backend implementation for Milvus and Zilliz Cloud."""

    def __init__(self) -> None:
        self._client: MilvusClient | None = None

    def _ensure_pymilvus(self) -> None:
        if MilvusClient is None:
            raise BackendError("milvus", "pymilvus is not installed. Run: pip install vectorfuse[milvus]")

    def _ensure_connected(self) -> None:
        if self._client is None:
            raise BackendError("milvus", "Not connected. Call connect() first.")

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def connect(self, **kwargs: Any) -> None:
        self._ensure_pymilvus()
        self._client = MilvusClient(**kwargs)

    def disconnect(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None

    def is_connected(self) -> bool:
        return self._client is not None

    # ------------------------------------------------------------------
    # Collections
    # ------------------------------------------------------------------

    def create_collection(self, name: str, schema: CollectionSchema) -> CollectionInfo:
        self._ensure_connected()
        # TODO: Translate CollectionSchema -> Milvus collection params
        raise NotImplementedError

    def drop_collection(self, name: str) -> None:
        self._ensure_connected()
        raise NotImplementedError

    def has_collection(self, name: str) -> bool:
        self._ensure_connected()
        raise NotImplementedError

    def list_collections(self) -> list[str]:
        self._ensure_connected()
        raise NotImplementedError

    def describe_collection(self, name: str) -> CollectionInfo:
        self._ensure_connected()
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Index management
    # ------------------------------------------------------------------

    def create_index(self, collection: str, config: IndexConfig) -> None:
        self._ensure_connected()
        raise NotImplementedError

    def drop_index(self, collection: str) -> None:
        self._ensure_connected()
        raise NotImplementedError

    def describe_index(self, collection: str) -> IndexInfo | None:
        self._ensure_connected()
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Vector CRUD
    # ------------------------------------------------------------------

    def upsert(self, collection: str, request: UpsertRequest) -> UpsertResult:
        self._ensure_connected()
        raise NotImplementedError

    def get(self, collection: str, ids: list[str], include_vectors: bool = False) -> GetResult:
        self._ensure_connected()
        raise NotImplementedError

    def delete(self, collection: str, ids: list[str]) -> DeleteResult:
        self._ensure_connected()
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(self, collection: str, request: SearchRequest) -> SearchResult:
        self._ensure_connected()
        raise NotImplementedError

    def hybrid_search(self, collection: str, request: HybridSearchRequest) -> SearchResult:
        self._ensure_connected()
        raise NotImplementedError
