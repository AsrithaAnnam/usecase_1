\# Incident Report — Claims Backend Unavailable



\## Summary and impact



The Claims backend was deliberately stopped during a local incident exercise.

The health endpoint on port 5001 became unreachable. The frontend and

database containers stayed running.



\## Detection



Docker Compose showed that the backend had exited, and curl could not connect

to the health endpoint. Prometheus and Grafana evidence is saved in evidence/.



\## Timeline (UTC)



\- Incident started: \[timestamp from 03-incident-start-time.txt]

\- Backend failure captured: 2026-11-10T05:26:00Z

\- Backend recovery confirmed by HTTP 200: 2026-11-10T09:41:54Z

\- Final platform verification: \[timestamp from 12-final-verification.txt]



\## Root cause and recovery



The outage was triggered by `docker compose stop backend`.

Running `docker compose start backend` restored the service.

The health endpoint returned HTTP 200 with status `healthy`.



\## Loki observation



The historical health-log query showed no matching logs during the

investigation. The Loki readiness endpoint later returned HTTP 200.



\## Prevention



Keep the recovery runbook current and test the availability alert.

For production deployments, use readiness checks, replicas, and

deployment validation to reduce the impact of a backend outage.
