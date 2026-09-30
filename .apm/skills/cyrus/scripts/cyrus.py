#!/usr/bin/env python3
"""cyrus: インタビュー型ドキュメント執筆ハーネスの CLI。

使い方: python3 cyrus.py --help
"""

import sys
from pathlib import Path

sys.dont_write_bytecode = True

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cyruslib.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
