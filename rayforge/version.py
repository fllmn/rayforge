import os
import logging
import subprocess
from typing import Optional

logger = logging.getLogger(__name__)

__dir__ = os.path.dirname(__file__)


def get_version_from_git() -> Optional[str]:
    logger.debug("Trying to source version from git")
    try:
        version = subprocess.check_output(
            ["git", "describe"], stderr=subprocess.DEVNULL, cwd=__dir__
        ).decode("ascii").strip()
    except (
        subprocess.CalledProcessError,
        FileNotFoundError,
        NotADirectoryError,
    ):
        logger.debug("Failed to source version from git")
        return None


    logger.debug(f"Using version sourced from git: {version}")
    return version


def get_version_from_pkg() -> Optional[str]:
    logger.debug("Trying to source version from pkg")
    try:
        from importlib.metadata import version, PackageNotFoundError
    except ImportError:
        return None

    try:
        output = version("rayforge")
        logger.debug(f"Using version sourced from pkg: {output}")
        return output
    except PackageNotFoundError:
        logger.debug("Failed to source version from pkg")
        return None


def get_version_from_file() -> Optional[str]:

    logger.debug("Trying to source version from version.txt")
    version_file = os.path.join(__dir__, "version.txt")
    try:
        with open(version_file, "r") as f:
            version = f.read().strip()
            logger.debug(f"Using version sourced from version.txt: {version}")
            return version
    except FileNotFoundError:
        logger.debug("Failed to source version from version.txt")
        return None
