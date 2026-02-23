"""Exceptions for vectorfuse."""


class VectorFuseError(Exception):
    """Base exception for all vectorfuse errors."""


class BackendNotFoundError(VectorFuseError):
    """Raised when a requested backend is not registered or installed."""

    def __init__(self, backend: str) -> None:
        self.backend = backend
        super().__init__(f"Backend '{backend}' not found. Is the extra installed? (pip install vectorfuse[{backend}])")


class CollectionNotFoundError(VectorFuseError):
    """Raised when a collection does not exist."""

    def __init__(self, collection: str) -> None:
        self.collection = collection
        super().__init__(f"Collection '{collection}' not found")


class CollectionAlreadyExistsError(VectorFuseError):
    """Raised when trying to create a collection that already exists."""

    def __init__(self, collection: str) -> None:
        self.collection = collection
        super().__init__(f"Collection '{collection}' already exists")


class DimensionMismatchError(VectorFuseError):
    """Raised when vector dimensions don't match the collection schema."""

    def __init__(self, expected: int, got: int) -> None:
        self.expected = expected
        self.got = got
        super().__init__(f"Dimension mismatch: collection expects {expected}, got {got}")


class ConnectionError(VectorFuseError):
    """Raised when the backend connection fails."""


class BackendError(VectorFuseError):
    """Raised when the backend returns an unexpected error."""

    def __init__(self, backend: str, message: str) -> None:
        self.backend = backend
        super().__init__(f"[{backend}] {message}")
