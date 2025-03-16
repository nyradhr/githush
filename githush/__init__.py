__version__ = "0.1.0"

from githush.cli import main
from githush.scan import scan_path

__all__ = ["main", "scan_path"]