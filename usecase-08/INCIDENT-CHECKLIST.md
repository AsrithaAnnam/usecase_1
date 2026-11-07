\# Claims Backend Incident Checklist



1\. Check `/api/health` to confirm whether the backend responds.

2\. Check Prometheus Targets for the `claims-backend` scrape status.

3\. Review request rate, HTTP 5xx rate, response time, and backend logs in Grafana.

4\. Confirm user impact and review recent changes.

5\. Restart or roll back the affected service if the evidence supports that action.

6\. Verify recovery through backend health, Prometheus, Grafana, and Loki.

7\. Record the timeline, cause, mitigation, recovery evidence, and follow-up work.



\## Controlled outage test



\- Cause: The backend container was stopped intentionally.

\- Detection: `ClaimsBackendDown` entered Firing after sustained scrape failures.

\- Recovery: The backend was restarted and the alert returned to Inactive.

\- Evidence: `evidence/13-alert-firing.json` and `evidence/14-alert-recovered.json`.

