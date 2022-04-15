#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8000
ENDPOINT = "/air_quality_alerts"


class CustomHandler(BaseHTTPRequestHandler):
    def _response(self, status: int, msg: str):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(msg.encode())

    def do_POST(self):
        if not self.path.startswith(ENDPOINT):
            self.log_error("Wrong endpoint")
            self._response(404, "Wrong endpoint")
            return
        if self.headers.get("Content-Type") != "application/ld+json":
            self.log_error("JSON-LD expected")
            self._response(415, "JSON-LD expected")
            return
        length = int(self.headers["Content-Length"])
        content = self.rfile.read(length)
        self.log_message(f"Notification received :\n{content.decode('utf-8')}")
        self._response(200, "OK")


def main():
    argc, argv = len(sys.argv), sys.argv
    port: int = PORT
    if argc > 2:
        sys.exit(1)
    elif argc == 2:
        try:
            port = int(argv[1])
        except ValueError:
            sys.exit(2)
    httpd = HTTPServer(("0.0.0.0", port), CustomHandler)
    httpd.allow_reuse_address = True
    print("Start HTTP Server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    print("\nStop HTTP Server")


if __name__ == "__main__":
    main()
