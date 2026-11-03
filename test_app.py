import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

import app

# Talk to the local test server directly, ignoring any proxy settings
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


class AppTest(unittest.TestCase):
    def setUp(self):
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), app.Handler)
        self.base = f"http://127.0.0.1:{self.server.server_port}"
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()

    def get(self, path):
        try:
            with OPENER.open(self.base + path) as resp:
                return resp.status, resp.read().decode()
        except urllib.error.HTTPError as err:
            with err:
                return err.code, err.read().decode()

    def test_hello(self):
        status, body = self.get("/")
        self.assertEqual(status, 200)
        self.assertIn("Hello, World!", body)

    def test_healthz(self):
        self.assertEqual(self.get("/healthz"), (200, "ok\n"))

    def test_unknown_path(self):
        status, _ = self.get("/nope")
        self.assertEqual(status, 404)


if __name__ == "__main__":
    unittest.main()
