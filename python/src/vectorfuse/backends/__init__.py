"""Backend registry - maps backend names to implementations."""

from __future__ import annotations

from typing import TYPE_CHECKING

from vectorfuse.exceptions import BackendNotFoundError

if TYPE_CHECKING:
    from vectorfuse.backends.base import Backend

# Registry of backend name -> import path (lazy loading)
_BACKEND_REGISTRY: dict[str, str] = {
    "milvus": "vectorfuse.backends.milvus.MilvusBackend",
    "zilliz": "vectorfuse.backends.milvus.MilvusBackend",  # alias
}


def get_backend(name: str) -> Backend:
    """Instantiate a backend by name.

    Args:
        name: Backend identifier (e.g., "milvus", "zilliz").

    Returns:
        An unconnected Backend instance.

    Raises:
        BackendNotFoundError: If the backend name is not registered.
    """
    import_path = _BACKEND_REGISTRY.get(name.lower())
    if import_path is None:
        raise BackendNotFoundError(name)

    module_path, class_name = import_path.rsplit(".", 1)

    try:
        import importlib

        module = importlib.import_module(module_path)
        backend_class = getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        raise BackendNotFoundError(name) from e

    return backend_class()


def register_backend(name: str, import_path: str) -> None:
    """Register a custom backend.

    Args:
        name: Backend identifier.
        import_path: Fully qualified class path (e.g., "mypackage.backends.CustomBackend").
    """
    _BACKEND_REGISTRY[name.lower()] = import_path


def list_backends() -> list[str]:
    """List all registered backend names."""
    return sorted(set(_BACKEND_REGISTRY.keys()))
