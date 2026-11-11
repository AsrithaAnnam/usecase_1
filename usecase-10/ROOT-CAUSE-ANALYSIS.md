\# Use Case 10 — GitLab Runner Failure and Recovery



\## Symptom

The usecase\_10\_ci\_health job stayed Pending because no eligible runner picked it up. The unit\_tests job passed on a separate runner.



\## First check

I checked the dedicated runner's status, its usecase-10 tag, and whether it could run jobs on the feature branch.



\## Root cause and recovery

I paused the dedicated runner to reproduce the queue issue. After I resumed it, the job stayed Pending. I restarted the GitLab Runner process in WSL, and the same job ran and passed. The reason it stayed Pending after resuming was not confirmed.



\## Validation

The runner, Docker, disk, GitLab Container Registry connectivity, and registry login checks passed on the same commit without any application code changes.



\- Pipeline: https://gitlab.com/AsrithaAnnam/usecase\_1/-/pipelines/3053995071

\- Health job: https://gitlab.com/AsrithaAnnam/usecase\_1/-/jobs/17931390993

\- Tested commit: f9cfc509656c92c7002471946d51876ee8476730



\## Prevention

When a job stays Pending, check the runner's pause state, job tag, and branch eligibility. For this WSL setup, also confirm that the GitLab Runner process is running.

