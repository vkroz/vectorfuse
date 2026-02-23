/**
 * vectorfuse — Unified API layer for vector database backends.
 */

export { VectorFuse, registerBackend, listBackends } from "./client.js";
export type { VectorFuseOptions } from "./client.js";

export type { Backend } from "./backends/base.js";
export { MilvusBackend } from "./backends/milvus.js";

export {
  DistanceMetric,
  IndexType,
  type CollectionSchema,
  type CollectionInfo,
  type IndexConfig,
  type IndexInfo,
  type UpsertRequest,
  type UpsertResult,
  type GetResult,
  type DeleteResult,
  type SearchRequest,
  type SearchMatch,
  type SearchResult,
  type HybridSearchRequest,
} from "./models.js";

export {
  VectorFuseError,
  BackendNotFoundError,
  CollectionNotFoundError,
  CollectionAlreadyExistsError,
  DimensionMismatchError,
  ConnectionError,
  BackendError,
} from "./exceptions.js";
