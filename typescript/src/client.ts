/**
 * VectorFuse client — the main entry point for all vector operations.
 */

import type { Backend } from "./backends/base.js";
import { MilvusBackend } from "./backends/milvus.js";
import { BackendNotFoundError } from "./exceptions.js";
import {
  DistanceMetric,
  IndexType,
  type CollectionInfo,
  type CollectionSchema,
  type DeleteResult,
  type GetResult,
  type HybridSearchRequest,
  type IndexConfig,
  type IndexInfo,
  type SearchRequest,
  type SearchResult,
  type UpsertRequest,
  type UpsertResult,
} from "./models.js";

// ---------------------------------------------------------------------------
// Backend registry
// ---------------------------------------------------------------------------

type BackendFactory = () => Backend;

const BACKEND_REGISTRY: Record<string, BackendFactory> = {
  milvus: () => new MilvusBackend(),
  zilliz: () => new MilvusBackend(),
};

export function registerBackend(name: string, factory: BackendFactory): void {
  BACKEND_REGISTRY[name.toLowerCase()] = factory;
}

export function listBackends(): string[] {
  return [...new Set(Object.keys(BACKEND_REGISTRY))].sort();
}

// ---------------------------------------------------------------------------
// Client options
// ---------------------------------------------------------------------------

export interface VectorFuseOptions {
  backend: string;
  [key: string]: unknown;
}

// ---------------------------------------------------------------------------
// VectorFuse client
// ---------------------------------------------------------------------------

export class VectorFuse {
  private readonly backendName: string;
  private readonly backend: Backend;

  constructor(private readonly options: VectorFuseOptions) {
    this.backendName = options.backend.toLowerCase();
    const factory = BACKEND_REGISTRY[this.backendName];
    if (!factory) {
      throw new BackendNotFoundError(this.backendName);
    }
    this.backend = factory();
  }

  async connect(): Promise<void> {
    const { backend: _, ...params } = this.options;
    await this.backend.connect(params);
  }

  async close(): Promise<void> {
    await this.backend.disconnect();
  }

  get isConnected(): boolean {
    return this.backend.isConnected();
  }

  // ------------------------------------------------------------------
  // Collections
  // ------------------------------------------------------------------

  async createCollection(
    name: string,
    opts: {
      dimension: number;
      metric?: DistanceMetric;
      description?: string;
    }
  ): Promise<CollectionInfo> {
    const schema: CollectionSchema = {
      dimension: opts.dimension,
      metric: opts.metric ?? DistanceMetric.COSINE,
      description: opts.description ?? "",
    };
    return this.backend.createCollection(name, schema);
  }

  async dropCollection(name: string): Promise<void> {
    return this.backend.dropCollection(name);
  }

  async hasCollection(name: string): Promise<boolean> {
    return this.backend.hasCollection(name);
  }

  async listCollections(): Promise<string[]> {
    return this.backend.listCollections();
  }

  async describeCollection(name: string): Promise<CollectionInfo> {
    return this.backend.describeCollection(name);
  }

  // ------------------------------------------------------------------
  // Index management
  // ------------------------------------------------------------------

  async createIndex(
    collection: string,
    opts?: {
      indexType?: IndexType;
      metric?: DistanceMetric;
      params?: Record<string, unknown>;
    }
  ): Promise<void> {
    const config: IndexConfig = {
      indexType: opts?.indexType ?? IndexType.AUTOINDEX,
      metric: opts?.metric ?? DistanceMetric.COSINE,
      params: opts?.params ?? {},
    };
    return this.backend.createIndex(collection, config);
  }

  async dropIndex(collection: string): Promise<void> {
    return this.backend.dropIndex(collection);
  }

  async describeIndex(collection: string): Promise<IndexInfo | null> {
    return this.backend.describeIndex(collection);
  }

  // ------------------------------------------------------------------
  // Vector CRUD
  // ------------------------------------------------------------------

  async upsert(
    collection: string,
    data: {
      ids: string[];
      vectors: number[][];
      metadata?: Record<string, unknown>[];
    }
  ): Promise<UpsertResult> {
    const request: UpsertRequest = {
      ids: data.ids,
      vectors: data.vectors,
      metadata: data.metadata,
    };
    return this.backend.upsert(collection, request);
  }

  async get(
    collection: string,
    ids: string[],
    opts?: { includeVectors?: boolean }
  ): Promise<GetResult> {
    return this.backend.get(collection, ids, opts?.includeVectors ?? false);
  }

  async delete(collection: string, ids: string[]): Promise<DeleteResult> {
    return this.backend.delete(collection, ids);
  }

  // ------------------------------------------------------------------
  // Search
  // ------------------------------------------------------------------

  async search(
    collection: string,
    opts: {
      queryVector: number[];
      topK?: number;
      filter?: Record<string, unknown>;
      includeVectors?: boolean;
      includeMetadata?: boolean;
      params?: Record<string, unknown>;
    }
  ): Promise<SearchResult> {
    const request: SearchRequest = {
      queryVector: opts.queryVector,
      topK: opts.topK ?? 10,
      filter: opts.filter,
      includeVectors: opts.includeVectors ?? false,
      includeMetadata: opts.includeMetadata ?? true,
      params: opts.params ?? {},
    };
    return this.backend.search(collection, request);
  }

  async hybridSearch(
    collection: string,
    opts: {
      denseVector: number[];
      sparseVector?: Record<number, number>;
      topK?: number;
      alpha?: number;
      filter?: Record<string, unknown>;
      includeVectors?: boolean;
      includeMetadata?: boolean;
      params?: Record<string, unknown>;
    }
  ): Promise<SearchResult> {
    const request: HybridSearchRequest = {
      denseVector: opts.denseVector,
      sparseVector: opts.sparseVector,
      topK: opts.topK ?? 10,
      alpha: opts.alpha ?? 0.5,
      filter: opts.filter,
      includeVectors: opts.includeVectors ?? false,
      includeMetadata: opts.includeMetadata ?? true,
      params: opts.params ?? {},
    };
    return this.backend.hybridSearch(collection, request);
  }
}
