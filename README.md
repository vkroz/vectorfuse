# vectorfuse

Unified API layer for vector database backends. Build applications that produce and consume embeddings without coupling to a specific vector DB vendor. Drop-in backend replacement without refactoring application code.

## Why

Your ML platform shouldn't care whether embeddings live in Milvus, Qdrant, Pinecone, or pgvector. **vectorfuse** provides a single interface — swap the backend config, keep your application code untouched.

## Packages

| Package | Path | Status |
|---------|------|--------|
| `vectorfuse` (Python) | [`python/`](./python) | 🚧 In progress |
| `vectorfuse` (TypeScript) | [`typescript/`](./typescript) | 🚧 In progress |

## Supported Backends

| Backend | Python | TypeScript |
|---------|--------|------------|
| Milvus / Zilliz | 🚧 | 🚧 |

## Quick Example

### Python

```python
from vectorfuse import VectorFuse

mux = VectorFuse(backend="milvus", uri="http://localhost:19530")

# Create a collection
mux.create_collection("documents", dimension=768)

# Upsert vectors
mux.upsert("documents", ids=["doc1", "doc2"], vectors=[vec1, vec2], metadata=[{"src": "web"}, {"src": "pdf"}])

# Search
results = mux.search("documents", query_vector=query_vec, top_k=10, filter={"src": "web"})
```

### TypeScript

```typescript
import { VectorFuse } from "vectorfuse";

const mux = new VectorFuse({ backend: "milvus", uri: "http://localhost:19530" });

await mux.createCollection("documents", { dimension: 768 });

await mux.upsert("documents", {
  ids: ["doc1", "doc2"],
  vectors: [vec1, vec2],
  metadata: [{ src: "web" }, { src: "pdf" }],
});

const results = await mux.search("documents", {
  queryVector: queryVec,
  topK: 10,
  filter: { src: "web" },
});
```

## Documentation

See [`docs/`](./docs) for architecture, API reference, and backend implementation guides.

## License

MIT
