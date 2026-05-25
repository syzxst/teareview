import json
import os
from http.server import BaseHTTPRequestHandler

# 用环境变量模拟简单存储，也可以换成数据库
COMMENTS_FILE = "/tmp/comments.json"

def init_comments():
    if not os.path.exists(COMMENTS_FILE):
        with open(COMMENTS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        init_comments()
        if self.path == "/api/comments":
            with open(COMMENTS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        init_comments()
        if self.path == "/api/comments":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_comment = json.loads(post_data.decode("utf-8"))

            with open(COMMENTS_FILE, "r", encoding="utf-8") as f:
                comments = json.load(f)
            comments.append(new_comment)
            with open(COMMENTS_FILE, "w", encoding="utf-8") as f:
                json.dump(comments, f, ensure_ascii=False, indent=2)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
