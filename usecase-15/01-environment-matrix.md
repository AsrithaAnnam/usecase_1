# Use Case 15 Environment Matrix

| Setting | Dev | QA | Stage | Prod-like |
|---|---|---|---|---|
| Namespace | claims-dev | claims-qa | claims-stage | claims-prod |
| Replicas | 1 | 1 | 2 | 3 |
| Image | Same digest | Same digest | Same digest | Same digest |
| Secret name | claims-dev-secret | claims-qa-secret | claims-stage-secret | claims-prod-secret |
| Approval | No | No | Required | Required |
| CPU request | 25m | 50m | 100m | 200m |
| Memory request | 32Mi | 64Mi | 128Mi | 256Mi |
| Monitoring | Basic | Test alerts | Production-like | Full |
| Rollback | helm rollback | helm rollback | helm rollback | helm rollback |

## Promotion flow

Development -> QA -> Stage -> Production

The image is built once and promoted by immutable digest.
