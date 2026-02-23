# vectorfuse (Python)

Unified Python API for vector database backends.

## Installation

```bash
# Core (no backends)
pip install vectorfuse

# With Milvus backend
pip install vectorfuse[milvus]

# All backends
pip install vectorfuse[all]
```

## Usage

```python
from vectorfuse import VectorFuse

mux = VectorFuse(backend="milvus", uri="http://localhost:19530")

mux.create_collection("my_collection", dimension=768)
mux.upsert("my_collection", ids=["id1"], vectors=[[0.1] * 768])
results = mux.search("my_collection", query_vector=[0.1] * 768, top_k=5)
```

## Development

```bash
cd python
uv sync --extra dev --extra milvus
uv run pytest
uv run ruff check .
```
