"""
Compatible with file managers like Nautilus, Nemo, and other XDG-compliant file managers.
Reads thumbnail cache for Ubuntu-like systems using the freedesktop.org thumbnail specification.
"""

import hashlib
import logging
from pathlib import Path
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# TODO function: get thumbnail path for a single file

# TODO for pdfs: read cover page (and other pages) to generate higher resolution images

def get_file_thumbnail_dict(files_dir_path: str | Path, cache_path: str | Path = "~/.cache") -> Dict[str, Optional[str]]:
    """Returns a dictionary with filenames as keys and their thumbnail paths as values.
    IMPORTANT: Function assumes that thumbnails are stored following freedesktop.org thumbnail specs.
            Read them here https://specifications.freedesktop.org/thumbnail/latest/thumbsave.html

    Args:
        files_dir_path: Path to directory containing files to find thumbnails for
        cache_path: Path to cache directory (default: ~/.cache)
        
    Returns:
        Dict mapping filenames to thumbnail paths (or None if no thumbnail exists)
        
    Raises:
        FileNotFoundError: If files_dir_path doesn't exist
    """
    logger.info("Getting file_thumbnail_dict.")
    logger.debug('Path cwd: %s', Path.cwd())
    
    # This will be the output dict
    file_thumbnail_dict: Dict[str, Optional[str]] = {}
    
    # Relative paths to absolute paths
    files_dir = Path(files_dir_path).expanduser().resolve()
    cache_dir = Path(cache_path).expanduser().resolve()

    if not files_dir.exists():
        raise FileNotFoundError(f"Files directory does not exist: {files_dir}")

    # Seems that pdf thumbnails are stored in ~/.cache/thumbnails/large
    normal_dir = cache_dir / 'thumbnails' / 'normal'
    large_dir = cache_dir / 'thumbnails' / 'large'

    normal_thumbnails = set(i.name for i in normal_dir.iterdir()) if normal_dir.exists() else set()
    large_thumbnails = set(i.name for i in large_dir.iterdir()) if large_dir.exists() else set()

    for file_path in files_dir.iterdir():
        if not file_path.is_file():
            continue

        f_uri = file_path.as_uri()

        # Thumbnail filenames are MD5 hashes of file URI
        expected_thumbnail_name = hashlib.md5(f_uri.encode('utf-8')).hexdigest()+ '.png'

        if expected_thumbnail_name in normal_thumbnails:
            logger.info("File %s was found in normal.", file_path.name)
            file_thumbnail_dict[file_path.name] = str(normal_dir / expected_thumbnail_name)
        elif expected_thumbnail_name in large_thumbnails:
            logger.info("File %s was found in large.", file_path.name)
            file_thumbnail_dict[file_path.name] = str(large_dir / expected_thumbnail_name)
        else:
            logger.warning("Didn't find %s", file_path.name)
            file_thumbnail_dict[file_path.name] = None
    
    return file_thumbnail_dict



if __name__ == "__main__":

    logger.info('Path cwd: %s', Path.cwd())
    logger.info('__file__: %s', __file__)
    
    result = get_file_thumbnail_dict(files_dir_path = '~/Documents/papers')
    logger.info(result)
