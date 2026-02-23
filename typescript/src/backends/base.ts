/**
 * Abstract backend interface — the contract all backends must implement.
 */

import type {
  CollectionInfo,
  CollectionSchema,
  DeleteResult,
  GetResult,
  HybridSearchRequest,
  IndexConfig,
  IndexInfo,
  SearchRequest,
  SearchResult,
  UpsertRequest,
  UpsertResult,
} from "../models.js";

export interface Backend {
  // Lifecycle
  connect(params: Record<string, unknown>): Promise<void>;
  disconnect(): Promise<void>;
  isConnected(): boolean;

  // Collections
  createCollection(name: string, schema: CollectionSchema): Promise<CollectionInfo>;
  dropCollection(name: string): Promise<void>;
  hasCollection(name: string): Promise<boolean>;
  listCollections(): Promise<string[]>;
  describeCollection(name: string): Promise<CollectionInfo>;

  // Index management
  createIndex(collection: string, config: IndexConfig): Promise<void>;
  dropIndex(collection: string): Promise<void>;
  describeIndex(collection: string): Promise<IndexInfo | null>;

  // Vector CRUD
  upsert(collection: string, request: UpsertRequest): Promise<UpsertResult>;
  get(collection: string, ids: string[], includeVectors?: boolean): Promise<GetResult>;
  delete(collection: string, ids: string[]): Promise<DeleteResult>;

  // Search
  search(collection: string, request: SearchRequest): Promise<SearchResult>;
  hybridSearch(collection: string, request: HybridSearchRequest): Promise<SearchResult>;
}
