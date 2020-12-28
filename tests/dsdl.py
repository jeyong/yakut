# Copyright (c) 2019 UAVCAN Consortium
# This software is distributed under the terms of the MIT License.
# Author: Pavel Kirienko <pavel@uavcan.org>

import sys
import pathlib
import importlib
import pytest


# Please maintain these carefully if you're changing the project's directory structure.
TEST_DIR = pathlib.Path(__file__).parent
ROOT_DIR = TEST_DIR.parent
OUTPUT_DIR = ROOT_DIR / pathlib.Path(".dsdl_generated")


@pytest.fixture(scope="session")  # type: ignore
def regulated_dsdl() -> pathlib.Path:
    """
    Ensures that the regulated DSDL namespaces are compiled and importable.
    To force recompilation, remove the output directory.
    """
    output_dir = str(OUTPUT_DIR)
    if output_dir not in sys.path:
        sys.path.insert(0, output_dir)
    try:
        import uavcan
    except ImportError:
        from tests.subprocess import execute_u
        from u.paths import DEFAULT_PUBLIC_REGULATED_DATA_TYPES_ARCHIVE_URI

        args = ["compile", DEFAULT_PUBLIC_REGULATED_DATA_TYPES_ARCHIVE_URI, "--output", output_dir]
        execute_u(*args, timeout=90.0)

        importlib.invalidate_caches()
        # noinspection PyUnresolvedReferences
        import uavcan

    return pathlib.Path(uavcan.__file__).parent.parent
