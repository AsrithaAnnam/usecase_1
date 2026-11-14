\# Use Case 12 — Rollback and Recovery


\## Rollback procedure


1\. Retrieve the last known-good API token version from Vault.

2\. Update the `API\_TOKEN` key in `claims-usecase12-secret` in the `claims-k8s-lab` namespace.

3\. Restart `deployment/claims-backend` and wait for the rollout to succeed.

4\. Verify that the new Pod loaded the restored token without printing its value.

5\. Call `/api/health` and confirm HTTP 200 with `"status":"healthy"`.


\## Recovery test result

Deleting the Kubernetes Secret caused the new backend Pod to show

`CreateContainerConfigError`. The old Pod stayed running. After I recreated

the Secret from Vault, the new Pod became `1/1 Running` with zero restarts.

The health endpoint returned HTTP 200. See `evidence/07-health-after-recovery.txt`.


\## Vault version history

The original Vault dev server stored its data in memory. Stopping it erased

the original version history. I copied the active token from Kubernetes into

the fresh Vault instance. It was version 2 before the restart and version 1

in the fresh instance.

The missing-Secret test confirmed recovery of the active token. The rollback

procedure above requires a retained earlier version. The evidence and current

backend log checks covered only the recovered token.