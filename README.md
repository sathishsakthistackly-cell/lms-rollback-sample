# LMS Rollback Sample

A small Flask web application to practise Docker deployment, Jenkins CI/CD, Nginx reverse proxying, health checks, and rollback.

## Project structure

```text
lms-rollback-sample/
├── app.py
├── Dockerfile
├── .dockerignore
├── Jenkinsfile
├── README.md
├── requirements.txt
├── scripts/
│   └── deploy-rollback.sh
├── nginx/
│   └── lms.conf
└── docs/
    └── implementation-notes.md
```

## Run locally

Requires Python 3.10+.

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000. Health endpoint: `/health`; version endpoint: `/version`.

## Build and run with Docker

```bash
docker build -t lms-rollback-sample:local .
docker run --rm -d --name lms-demo -p 8080:5000 -e APP_VERSION=local -e ENVIRONMENT=demo lms-rollback-sample:local
```

Visit http://localhost:8080/health. Stop with `docker rm -f lms-demo`.

## Jenkins and Nginx

The Jenkins agent needs Docker access and curl. Configure a Pipeline job from this repository. The Nginx config forwards port 80 to the app on host port 8080; adjust the upstream if needed. Validate Nginx with `nginx -t` before reloading.

## Rollback

The script polls the health endpoint. If checks fail, it prints container logs and attempts to restart the previous image. Test this in a disposable environment first; this is a learning sample, not production-ready deployment automation.
