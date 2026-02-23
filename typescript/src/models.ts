/**
 * Data models for vectorfuse unified API.
 * Mirrors the Python models for cross-language consistency.
 */

// ---------------------------------------------------------------------------
// Enums
// ---------------------------------------------------------------------------

export enum DistanceMetric {
  COSINE = "cosine",
  L2 = "l2",
  IP = "ip",
}

export enum IndexType {
  FLAT = "flat",
  IVF_FLAT = "ivf_flat",
  IVF_SQ8 = "ivf_sq8",
  IVF_PQ = "ivf_pq",
  HNSW = "hnsw",
  AUTOINDEX = "autoindex",
}

// ---------------------------------------------------------------------------
// Collection
// ---------------------------------------------------------------------------

export interface CollectionSchema {
  dimension: number;
  metric?: DistanceMetric;
  description?: string;
}

export interface CollectionInfo {
  name: string;
  dimension: number;
  metric: DistanceMetric;
  vectorCount: number;
  description: string;
}

// ---------------------------------------------------------------------------
// Index
// ---------------------------------------------------------------------------

export interface IndexConfig {
  indexType?: IndexType;
  metric?: DistanceMetric;
  params?: Record<string, unknown>;
}

export interface IndexInfo {
  fieldName: string;
  indexType: IndexType;
  metric: DistanceMetric;
  params: Record<string, unknown>;
}

// ---------------------------------------------------------------------------
// Vector operations
// ---------------------------------------------------------------------------

export interface UpsertRequest {
  ids: string[];
  vectors: number[][];
  metadata?: Record<string, unknown>[];
}

export interface UpsertResult {
  upsertedCount: number;
  ids: string[];
}

export interface GetResult {
  ids: string[];
  vectors?: number[][];
  metadata?: Record<string, unknown>[];
}

export interface DeleteResult {
  deletedCount: number;
}

// ---------------------------------------------------------------------------
// Search
// ---------------------------------------------------------------------------

export interface SearchRequest {
  queryVector: number[];
  topK?: number;
  filter?: Record<string, unknown>;
  includeVectors?: boolean;
  includeMetadata?: boolean;
  params?: Record<string, unknown>;
}

export interface SearchMatch {
  id: string;
  score: number;
  vector?: number[];
  metadata?: Record<string, unknown>;
}

export interface SearchResult {
  matches: SearchMatch[];
  total: number;
}

// ---------------------------------------------------------------------------
// Hybrid search
// ---------------------------------------------------------------------------

export interface HybridSearchRequest {
  denseVector: number[];
  sparseVector?: Record<number, number>;
  topK?: number;
  /** Weight for dense vs sparse (1.0 = all dense) */
  alpha?: number;
  filter?: Record<string, unknown>;
  includeVectors?: boolean;
  includeMetadata?: boolean;
  params?: Record<string, unknown>;
}
