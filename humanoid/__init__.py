# This file makes the folder a package
import warnings

from .humanoid import Humanoid

warnings.filterwarnings(
    "ignore",
    message="Pydantic serializer warnings:",
    category=UserWarning,
    module="pydantic.main",
)

__version__ = "0.0.1"
__all__ = ["Humanoid"]
