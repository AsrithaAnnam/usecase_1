\# Use Case 09 — Simulate an Incident and Recover



This lab uses the local Claims application and the Use Case 08 monitoring

stack to practice detecting and recovering from a backend outage.



1\. Verify that the application and monitoring services are running.

2\. Generate normal traffic and capture the Prometheus request-rate graph.

3\. Stop the backend and verify that its health endpoint is unreachable.

4\. Check Prometheus targets and alerts, the Grafana dashboard, and Loki logs.

5\. Start the backend and verify application and monitoring recovery.



\- \[Incident report](INCIDENT-REPORT.md)

\- \[Recovery runbook](RUNBOOK.md)

\- \[Evidence](evidence/)
