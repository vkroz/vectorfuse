# Adding a New Backend

This guide walks through implementing a new vector DB backend for vectorfuse.

## Step 1: Implement the Backend Interface

Create a new file in `backends/` (e.g., `backends/qdrant.py`):

```python
from vectorfuse.backends.base import Backend
from vectorfuse.models import *
from vectorfuse.exceptions import *

class QdrantBackend(Backend):
    def connect(self, **kwargs):
        # Initialize the vendor SDK client
        ...

    def disconnect(self):
        ...

    # Implement all abstract methods...
```

## Step 2: Register the Backend

In `backends/__init__.py`, add to `_BACKEND_REGISTRY`:

```python
_BACKEND_REGISTRY = {
    "milvus": "vectorfuse.backends.milvus.MilvusBackend",
    "qdrant": "vectorfuse.backends.qdrant.QdrantBackend",  # new
}
```

## Step 3: Add the Dependency

In `pyproject.toml`:

```toml
[project.optional-dependencies]
qdrant = ["qdrant-client>=1.9"]
all = ["vectorfuse[milvus,qdrant]"]
```

## Step 4: Error Mapping

Map vendor-specific exceptions to vectorfuse exceptions:

| vectorfuse exception | When to raise |
|---|---|
| `CollectionNotFoundError` | Collection does not exist |
| `CollectionAlreadyExistsError` | Creating a duplicate collection |
| `DimensionMismatchError` | Vector dimensions don't match schema |
| `ConnectionError` | Cannot connect to backend |
| `BackendError` | Any other backend-specific error |

## Step 5: Tests

Add tests in `tests/test_<backend>.py`. At minimum, test:

- Connection lifecycle
- Collection CRUD
- Vector upsert and retrieval
- Similarity search with metadata filtering
- Error cases (missing collection, dimension mismatch)

## Checklist

- [ ] Implements all `Backend` abstract methods
- [ ] Registered in backend registry
- [ ] SDK added as optional dependency
- [ ] Vendor exceptions mapped to vectorfuse exceptions
- [ ] Tests pass
- [ ] TypeScript implementation mirrors Python
