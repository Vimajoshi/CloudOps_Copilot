# Kubernetes Deployment Rollout Failure

## Find the rollout blocker

Run `kubectl -n <namespace> rollout status deployment/<deployment>` and inspect the deployment, pods, and Events. Look for failed readiness probes, image pull errors, scheduling failures, and application startup errors. Compare the deployment revision and configuration with the last healthy release.

## Recover the deployment

Correct the confirmed issue in source and redeploy, or use `kubectl -n <namespace> rollout undo deployment/<deployment>` if the approved rollback policy permits. Monitor rollout status, ready replicas, and service error rate. Escalate if a rollback has data migration or compatibility implications.
