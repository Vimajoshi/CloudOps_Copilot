# Kubernetes OOMKilled

## Investigate memory termination

Use `kubectl -n <namespace> describe pod <pod>` to confirm the container's last termination reason is `OOMKilled` and inspect configured memory requests and limits. Compare memory usage and restart trends with application traffic and recent releases. Container OOMKilled can mean a container limit was hit; investigate node memory pressure separately.

## Recover and prevent recurrence

If a release introduced a leak, follow the approved rollback procedure. If normal peak usage exceeds the limit, review capacity and adjust requests and limits through a tested deployment change; do not simply remove the limit. Capture memory profiles where safe, investigate the leak, and verify memory and restarts after rollout.
