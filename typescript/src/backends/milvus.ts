/**
 * Milvus/Zilliz backend implementation.
 *
 * Requires peer dependency: @zilliz/milvus2-sdk-node
 */

import type { Backend } from "./base.js";
import { BackendError } from "../exceptions.js";
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

export class MilvusBackend implements Backend {
  private client: unknown | null = null;

  // ------------------------------------------------------------------
  // Lifecycle
  // ------------------------------------------------------------------

  async connect(params: Record<string, unknown>): Promise<void> {
    let MilvusClient: unknown;
    try {
      const mod = await import("@zilliz/milvus2-sdk-node");
      MilvusClient = mod.MilvusClient;
    } catch {
      throw new BackendError(
        "milvus",
        "@zilliz/milvus2-sdk-node is not installed. Run: npm install @zilliz/milvus2-sdk-node"
      );
    }
    this.client = new (MilvusClient as new (params: Record<string, unknown>) => unknown)(params);
  }

  async disconnect(): Promise<void> {
    this.client = null;
  }

  isConnected(): boolean {
    return this.client !== null;
  }

  private ensureConnected(): void {
    if (this.client === null) {
      throw new BackendError("milvus", "Not connected. Call connect() first.");
    }
  }

  // ------------------------------------------------------------------
  // Collections
  // ------------------------------------------------------------------

  async createCollection(name: string, schema: CollectionSchema): Promise<CollectionInfo> {
    this.ensureConnected();
    // TODO: Translate CollectionSchema -> Milvus collection params
    throw new Error("Not implemented");
  }

  async dropCollection(name: string): Promise<void> {
    this.ensureConnected();
    throw new Error("Not implemented");
  }

  async hasCollection(name: string): Promise<boolean> {
    this.ensureConnected();
    throw new Error("Not implemented");
  }

  async listCollections(): Promise<string[]> {
    this.ensureConnected();
    throw new Error("Not implemented");
  }

  async describeCollection(name: string): Promise<CollectionInfo> {
    this.ensureConnected();
    throw new Error("Not implemented");
  }

  // ------------------------------------------------------------------
  // Index management
  // ------------------------------------------------------------------

  async createIndex(collection: string, config: IndexConfig): Promise<void> {
    this.ensureConnected();
    throw new Error("Not implemented");
  }

  async dropIndex(collection: string): Promise<void> {
    this.ensureConnected();
    throw new Error("Not implemented");
  }

  async describeIndex(collection: string): Promise<IndexInfo | null> {
    this.ensureConnected();
    throw new Error("Not implemented");
  }

  // ------------------------------------------------------------------
  // Vector CRUD
  // ------------------------------------------------------------------

  async upsert(collection: string, request: UpsertRequest): Promise<UpsertResult> {
    this.ensureConnected();
    throw new Error("Not implemented");
  }

  async get(collection: string, ids: string[], includeVectors = false): Promise<GetResult> {
    this.ensureConnected();
    throw new Error("Not implemented");
  }

  async delete(collection: string, ids: string[]): Promise<DeleteResult> {
    this.ensureConnected();
    throw new Error("Not implemented");
  }

  // ------------------------------------------------------------------
  // Search
  // ------------------------------------------------------------------

  async search(collection: string, request: SearchRequest): Promise<SearchResult> {
    this.ensureConnected();
    throw new Error("Not implemented");
  }

  async hybridSearch(collection: string, request: HybridSearchRequest): Promise<SearchResult> {
    this.ensureConnected();
    throw new Error("Not implemented");
  }
}
