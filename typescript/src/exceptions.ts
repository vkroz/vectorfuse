/**
 * Exceptions for vectorfuse.
 */

export class VectorFuseError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "VectorFuseError";
  }
}

export class BackendNotFoundError extends VectorFuseError {
  public readonly backend: string;

  constructor(backend: string) {
    super(
      `Backend '${backend}' not found. Is the peer dependency installed?`
    );
    this.name = "BackendNotFoundError";
    this.backend = backend;
  }
}

export class CollectionNotFoundError extends VectorFuseError {
  public readonly collection: string;

  constructor(collection: string) {
    super(`Collection '${collection}' not found`);
    this.name = "CollectionNotFoundError";
    this.collection = collection;
  }
}

export class CollectionAlreadyExistsError extends VectorFuseError {
  public readonly collection: string;

  constructor(collection: string) {
    super(`Collection '${collection}' already exists`);
    this.name = "CollectionAlreadyExistsError";
    this.collection = collection;
  }
}

export class DimensionMismatchError extends VectorFuseError {
  public readonly expected: number;
  public readonly got: number;

  constructor(expected: number, got: number) {
    super(`Dimension mismatch: collection expects ${expected}, got ${got}`);
    this.name = "DimensionMismatchError";
    this.expected = expected;
    this.got = got;
  }
}

export class ConnectionError extends VectorFuseError {
  constructor(message: string) {
    super(message);
    this.name = "ConnectionError";
  }
}

export class BackendError extends VectorFuseError {
  public readonly backend: string;

  constructor(backend: string, message: string) {
    super(`[${backend}] ${message}`);
    this.name = "BackendError";
    this.backend = backend;
  }
}
