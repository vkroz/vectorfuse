"""Basic tests for vectorfuse package structure and models."""

import pytest

from vectorfuse import VectorFuse, __version__
from vectorfuse.backends import get_backend, list_backends
from vectorfuse.exceptions import BackendNotFoundError
from vectorfuse.models import (
    CollectionSchema,
    DistanceMetric,
    IndexConfig,
    IndexType,
    SearchRequest,
    UpsertRequest,
)


def test_version():
    assert __version__ == "0.1.0"


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TestModels:
    def test_collection_schema_defaults(self):
        schema = CollectionSchema(dimension=768)
        assert schema.dimension == 768
        assert schema.metric == DistanceMetric.COSINE
        assert schema.description == ""

    def test_collection_schema_validation(self):
        with pytest.raises(Exception):
            CollectionSchema(dimension=0)

    def test_upsert_request(self):
        req = UpsertRequest(ids=["a", "b"], vectors=[[0.1, 0.2], [0.3, 0.4]])
        assert len(req.ids) == 2
        assert req.metadata is None

    def test_upsert_request_with_metadata(self):
        req = UpsertRequest(
            ids=["a"],
            vectors=[[0.1, 0.2]],
            metadata=[{"source": "web"}],
        )
        assert req.metadata == [{"source": "web"}]

    def test_search_request_defaults(self):
        req = SearchRequest(query_vector=[0.1, 0.2, 0.3])
        assert req.top_k == 10
        assert req.filter is None
        assert req.include_metadata is True
        assert req.include_vectors is False

    def test_index_config_defaults(self):
        config = IndexConfig()
        assert config.index_type == IndexType.AUTOINDEX
        assert config.metric == DistanceMetric.COSINE

    def test_distance_metric_values(self):
        assert DistanceMetric.COSINE.value == "cosine"
        assert DistanceMetric.L2.value == "l2"
        assert DistanceMetric.IP.value == "ip"


# ---------------------------------------------------------------------------
# Backend registry tests
# ---------------------------------------------------------------------------


class TestBackendRegistry:
    def test_list_backends(self):
        backends = list_backends()
        assert "milvus" in backends
        assert "zilliz" in backends

    def test_unknown_backend_raises(self):
        with pytest.raises(BackendNotFoundError) as exc_info:
            get_backend("nonexistent")
        assert "nonexistent" in str(exc_info.value)
