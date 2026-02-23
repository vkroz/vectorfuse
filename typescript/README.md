# vectorfuse (TypeScript)

Unified TypeScript API for vector database backends.

## Installation

```bash
# Core
npm install vectorfuse

# With Milvus backend
npm install vectorfuse @zilliz/milvus2-sdk-node
```

## Usage

```typescript
import { VectorFuse } from "vectorfuse";

const mux = new VectorFuse({ backend: "milvus", uri: "http://localhost:19530" });
await mux.connect();

await mux.createCollection("my_collection", { dimension: 768 });
await mux.upsert("my_collection", { ids: ["id1"], vectors: [[0.1, ...]] });
const results = await mux.search("my_collection", { queryVector: [0.1, ...], topK: 5 });

await mux.close();
```

## Development

```bash
cd typescript
npm install
npm test
npm run build
```
