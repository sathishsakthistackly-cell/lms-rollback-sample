# Implementation Notes

## Purpose
Demonstrate a basic Flask app, Docker packaging, Jenkins pipeline, Nginx reverse proxy, health checks, and rollback.

## Request flow
1. Browser reaches Nginx on port 80.
2. Nginx forwards requests to host port 8080.
3. Docker maps port 8080 to Gunicorn/Flask port 5000.
4. `/health` returns status and version; `/version` reports app, version, environment, and container host.

## Rollback outline
1. Build a new image with a build-number tag.
2. Start the candidate container.
3. Poll the health endpoint.
4. If healthy, deployment succeeds.
5. If unhealthy, print logs and attempt to start the previous image.

## Limitations and safety
- Validate the Jenkins pipeline on your own Jenkins agent before use.
- A production implementation should store deployment metadata reliably, verify the rollback container, use a registry and immutable image digests, protect credentials, enable TLS, and add monitoring and access controls.
- Nginx expects the application at `127.0.0.1:8080` on the same host.
- Test failure paths in a non-production environment before deploying to a real LMS.

## Manual smoke test
```bash
curl -i http://127.0.0.1:8080/health
curl -i http://127.0.0.1:8080/version
```
