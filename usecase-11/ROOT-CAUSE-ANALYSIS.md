\# Use Case 11 — ImagePullBackOff and Registry Access



\## Problem



I deployed the Claims frontend to the `claims-k8s-lab` namespace on Docker Desktop Kubernetes using the deliberately missing tag `usecase-11-missing`. I used GitLab Container Registry for this lab.



\## Root cause and fix



The first pod events showed `403 Forbidden` for an anonymous registry request. After I attached a pull secret, GitLab returned `401 Unauthorized`. I verified that Docker could pull `usecase-11-good`, then updated `gitlab-pull-secret` with the same working credentials and restarted the Deployment. The new pod event returned `not found` for `usecase-11-missing`, confirming the deliberate tag error.



I switched the Deployment to `usecase-11-good`, and Kubernetes pulled the image successfully. NGINX then exited because it could not resolve `backend:5000`. I created a ClusterIP Service named `backend` on port 5000 so NGINX could resolve the hostname and start.



\## Verification



The Deployment rolled out successfully, and the frontend pod showed `1/1 Running` with zero restarts. This verified frontend startup. The `/api/` routes still require a running backend behind the Service.



\## Evidence



\- `evidence/07-image-pull-failure.txt` — Initial registry access failure

\- `evidence/15-pull-events-after-retry.txt` — Confirmed missing-tag error

\- `evidence/16-frontend-pod-details.txt` — Successful pull followed by container exit

\- `evidence/18-rollout-success.txt` — Successful rollout

\- `evidence/18-frontend-running.txt` — Frontend pod running and ready

\- `evidence/18-recovered-pod-details.txt` — Recovered pod details

