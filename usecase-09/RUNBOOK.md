\# Claims Backend Recovery Runbook



1\. Check `http://localhost:5001/api/health` and run `docker compose ps`.

2\. In Prometheus, check the `claims-backend` target and `ClaimsBackendDown` alert.

3\. Review the Grafana dashboard, Loki logs, Docker logs, and recent Git changes.

4\. If the backend is stopped, run `docker compose start backend`.

5\. Confirm HTTP 200, the Prometheus target UP, and the alert Inactive.

6\. Verify the platform health endpoints and record the UTC recovery time

&#x20;  and supporting evidence in the incident report.
