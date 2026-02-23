"""Data models for vectorfuse unified API."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class DistanceMetric(str, Enum):
    """Supported distance/similarity metrics."""

    COSINE = "cosine"
    L2 = "l2"
    IP = "ip"  # inner product


class IndexType(str, Enum):
    """Supported index types."""

    FLAT = "flat"
    IVF_FLAT = "ivf_flat"
    IVF_SQ8 = "ivf_sq8"
    IVF_PQ = "ivf_pq"
    HNSW = "hnsw"
    AUTOINDEX = "autoindex"


# ---------------------------------------------------------------------------
# Collection
# ---------------------------------------------------------------------------


class CollectionSchema(BaseModel):
    """Schema definition for a vector collection."""

    dimension: int = Field(..., gt=0, description="Dimensionality of vectors")
    metric: DistanceMetric = Field(default=DistanceMetric.COSINE, description="Distance metric for similarity search")
    description: str = Field(default="", description="Human-readable description")


class CollectionInfo(BaseModel):
    """Metadata about an existing collection."""

    name: str
    dimension: int
    metric: DistanceMetric
    vector_count: int = 0
    description: str = ""


# ---------------------------------------------------------------------------
# Index
# ---------------------------------------------------------------------------


class IndexConfig(BaseModel):
    """Configuration for creating an index."""

    index_type: IndexType = Field(default=IndexType.AUTOINDEX)
    metric: DistanceMetric = Field(default=DistanceMetric.COSINE)
    params: dict[str, Any] = Field(default_factory=dict, description="Backend-specific index parameters")


class IndexInfo(BaseModel):
    """Metadata about an existing index."""

    field_name: str
    index_type: IndexType
    metric: DistanceMetric
    params: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Vector operations
# ---------------------------------------------------------------------------


class UpsertRequest(BaseModel):
    """Request to upsert vectors into a collection."""

    ids: list[str] = Field(..., min_length=1)
    vectors: list[list[float]] = Field(..., min_length=1)
    metadata: list[dict[str, Any]] | None = Field(default=None, description="Per-vector metadata")


class UpsertResult(BaseModel):
    """Result of an upsert operation."""

    upserted_count: int
    ids: list[str]


class GetResult(BaseModel):
    """Result of a get-by-id operation."""

    ids: list[str]
    vectors: list[list[float]] | None = None
    metadata: list[dict[str, Any]] | None = None


class DeleteResult(BaseModel):
    """Result of a delete operation."""

    deleted_count: int


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------


class SearchRequest(BaseModel):
    """Request for similarity search."""

    query_vector: list[float]
    top_k: int = Field(default=10, gt=0)
    filter: dict[str, Any] | None = Field(default=None, description="Metadata filter expression")
    include_vectors: bool = Field(default=False, description="Whether to return vectors in results")
    include_metadata: bool = Field(default=True, description="Whether to return metadata in results")
    params: dict[str, Any] = Field(default_factory=dict, description="Backend-specific search parameters")


class SearchMatch(BaseModel):
    """A single search result."""

    id: str
    score: float
    vector: list[float] | None = None
    metadata: dict[str, Any] | None = None


class SearchResult(BaseModel):
    """Result of a similarity search."""

    matches: list[SearchMatch]
    total: int = 0


# ---------------------------------------------------------------------------
# Hybrid search
# ---------------------------------------------------------------------------


class HybridSearchRequest(BaseModel):
    """Request for hybrid (dense + sparse) search."""

    dense_vector: list[float]
    sparse_vector: dict[int, float] | None = Field(default=None, description="Sparse vector as {index: value}")
    top_k: int = Field(default=10, gt=0)
    alpha: float = Field(default=0.5, ge=0.0, le=1.0, description="Weight for dense vs sparse (1.0 = all dense)")
    filter: dict[str, Any] | None = None
    include_vectors: bool = False
    include_metadata: bool = True
    params: dict[str, Any] = Field(default_factory=dict)
