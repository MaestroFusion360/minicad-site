"""Serve the site from the repository root and report the bound address."""

import argparse
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--port", type=int, default=8000)
parser.add_argument("--ready-file", type=Path, required=True)
args = parser.parse_args()
handler = partial(
    SimpleHTTPRequestHandler, directory=str(Path(__file__).resolve().parent.parent)
)
try:
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
except OSError:
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
with server:
    args.ready_file.write_text(
        json.dumps({"url": f"http://127.0.0.1:{server.server_port}/"}),
        encoding="utf-8",
    )
    server.serve_forever()
