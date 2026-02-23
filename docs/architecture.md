# Architecture

## Overview

vectorfuse is a thin abstraction layer that sits between your application and vector database backends. It provides a unified interface so applications can produce and consume embeddings without knowing the underlying vendor.

```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   App A     │  │   App B     │  │   App C     │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
                 ┌──────▼──────┐
                 │  vectorfuse  │  ← unified API
                 │   client    │
                 └──────┬──────┘
                        │
              ┌─────────┼─────────┐
              │         │         │
       ┌──────▼───┐ ┌───▼────┐ ┌─▼────────┐
       │  Milvus  │ │ Qdrant │ │ Pinecone │   ← backends
       └──────────┘ └────────┘ └──────────┘
```

## Design Principles

1. **Backend-agnostic**: Applications code to the vectorfuse interface. Swapping backends is a config change, not a code change.
2. **Pre-computed vectors**: vectorfuse does NOT generate embeddings. It expects vectors to be computed upstream (by your embedding pipeline). This keeps concerns separated.
3. **Thin translation layer**: The library does minimal processing. It translates unified API calls into backend-specific SDK calls. No caching, no connection pooling beyond what the backend SDK provides.
4. **Consistent models across languages**: Python and TypeScript packages share the same data models and API shape.

## Key Components

### Client (`VectorFuse`)

The user-facing entry point. Accepts a backend name and connection params, delegates all operations to the selected backend.

### Backend (abstract interface)

Defines the contract every backend must implement:

- **Lifecycle**: `connect`, `disconnect`, `is_connected`
- **Collections**: `create_collection`, `drop_collection`, `has_collection`, `list_collections`, `describe_collection`
- **Index**: `create_index`, `drop_index`, `describe_index`
- **CRUD**: `upsert`, `get`, `delete`
- **Search**: `search`, `hybrid_search`

### Backend Registry

Maps backend names (e.g., `"milvus"`) to their implementations via lazy loading. Backends are only imported when selected, keeping the dependency footprint minimal.

Custom backends can be registered:

```python
from vectorfuse.backends import register_backend
register_backend("my_custom_db", "mypackage.backends.CustomBackend")
```

## Adding a New Backend

1. Create a new module in `backends/` that implements the `Backend` interface
2. Register it in the backend registry
3. Add the backend's SDK as an optional dependency
4. Add tests

See `backends/milvus.py` as a reference implementation.
