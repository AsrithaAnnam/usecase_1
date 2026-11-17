# Use Case 14 Rollout Stop Signals

### 1. Readiness
Stop promotion if the new Pod stays at 0/1 or the rollout exceeds the approved timeout.

### 2. Endpoints
Stop or roll back if the main Service has no endpoint or its EndpointSlice reports Ready=false.

### 3. HTTP errors
Stop or roll back if the health check fails to return HTTP 200 or the production 5xx rate exceeds the agreed threshold.

### 4. Latency
Stop or roll back if Green's p95 latency is materially higher than the Blue baseline.

### 5. Restarts
Stop or roll back if restarts increase or the new Pod enters CrashLoopBackOff.

### 6. Logs
Stop or roll back if logs show repeated exceptions, database failures, or dependency timeouts.

### 7. Business health
Stop or roll back if a critical action such as login or claim creation fails.
