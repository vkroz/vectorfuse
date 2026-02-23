"""vectorfuse — Unified API layer for vector database backends."""

from vectorfuse.client import VectorFuse
from vectorfuse.exceptions import (
    BackendError,
    BackendNotFoundError,
    CollectionAlreadyExistsError,
    CollectionNotFoundError,
    ConnectionError,
    DimensionMismatchError,
    VectorFuseError,
)
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

__version__ = "0.1.0"

__all__ = [
    # Client
    "VectorFuse",
    # Models
    "CollectionInfo",
    "CollectionSchema",
    "DeleteResult",
    "DistanceMetric",
    "GetResult",
    "HybridSearchRequest",
    "IndexConfig",
    "IndexInfo",
    "IndexType",
    "SearchMatch",
    "SearchRequest",
    "SearchResult",
    "UpsertRequest",
    "UpsertResult",
    # Exceptions
    "BackendError",
    "BackendNotFoundError",
    "CollectionAlreadyExistsError",
    "CollectionNotFoundError",
    "ConnectionError",
    "DimensionMismatchError",
    "VectorFuseError",
]
