"""Validation errors."""


class ConfigurationError(Exception):
    """Generic configuration error."""


class MissingRequiredKeyError(ConfigurationError):
    """Missing required key error."""


class MissingDependencyError(ConfigurationError):
    """Missing dependency error."""


class ValidationError(ConfigurationError):
    """Validation error."""


class KeyDeclarationError(ConfigurationError):
    """Key declaration error."""


class UnknownKeyError(ConfigurationError):
    """Unknown key error."""
