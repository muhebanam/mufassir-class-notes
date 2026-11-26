#!/usr/bin/env python3
"""লঞ্চার: python pipeline/jp.py <কমান্ড> …  (বিস্তারিত: pipeline/README.md)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jalalayn_pipeline.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
