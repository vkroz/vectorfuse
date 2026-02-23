import { describe, it, expect } from "vitest";
import { VectorFuse, listBackends, BackendNotFoundError, DistanceMetric, IndexType } from "../src/index.js";

describe("backend registry", () => {
  it("lists registered backends", () => {
    const backends = listBackends();
    expect(backends).toContain("milvus");
    expect(backends).toContain("zilliz");
  });

  it("throws on unknown backend", () => {
    expect(() => new VectorFuse({ backend: "nonexistent" })).toThrow(
      BackendNotFoundError
    );
  });
});

describe("enums", () => {
  it("DistanceMetric values", () => {
    expect(DistanceMetric.COSINE).toBe("cosine");
    expect(DistanceMetric.L2).toBe("l2");
    expect(DistanceMetric.IP).toBe("ip");
  });

  it("IndexType values", () => {
    expect(IndexType.HNSW).toBe("hnsw");
    expect(IndexType.AUTOINDEX).toBe("autoindex");
  });
});

describe("VectorFuse client", () => {
  it("instantiates with milvus backend", () => {
    const mux = new VectorFuse({ backend: "milvus", uri: "http://localhost:19530" });
    expect(mux.isConnected).toBe(false);
  });

  it("instantiates with zilliz alias", () => {
    const mux = new VectorFuse({ backend: "zilliz", uri: "https://in01-xxx.zillizcloud.com" });
    expect(mux.isConnected).toBe(false);
  });
});
