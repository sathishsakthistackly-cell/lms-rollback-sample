from flask import Flask, jsonify, render_template_string
import os, socket
from datetime import datetime, timezone

app = Flask(__name__)
VERSION = os.getenv("APP_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
PAGE = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>LMS Sample</title>
<style>body{font:16px Arial;background:#f3f6fb;color:#243247;margin:0}.card{max-width:700px;margin:8vh auto;background:white;padding:28px;border:1px solid #dce5f0;border-radius:14px}h1{color:#145da0}.tag{color:#145da0;background:#edf5ff;padding:6px 10px;border-radius:20px}dt{color:#64748b;margin-top:12px}dd{margin:4px 0;font-weight:bold}</style></head>
<body><main class="card"><span class="tag">Deployment demo</span><h1>Learning Management System</h1><p>Sample app for Docker deployment and rollback practice.</p>
<dl><dt>Version</dt><dd>{{ version }}</dd><dt>Environment</dt><dd>{{ environment }}</dd><dt>Container host</dt><dd>{{ hostname }}</dd><dt>Server time</dt><dd>{{ server_time }}</dd></dl><p>Endpoints: <code>/health</code> and <code>/version</code></p></main></body></html>"""

@app.get("/")
def index():
    return render_template_string(PAGE, version=VERSION, environment=ENVIRONMENT,
        hostname=socket.gethostname(), server_time=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"))

@app.get("/health")
def health():
    return jsonify(status="healthy", version=VERSION), 200

@app.get("/version")
def version():
    return jsonify(app="lms-rollback-sample", version=VERSION, environment=ENVIRONMENT,
                   hostname=socket.gethostname()), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
