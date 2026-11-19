# Kubernetes Pods Pending

## Inspect scheduling events

Use `kubectl -n <namespace> describe pod <pod>` and read scheduler Events for insufficient CPU or memory, taints, affinity, topology constraints, or volume binding. Compare requests with available node capacity and the intended scheduling rules.

## Resolve the scheduling constraint

Correct an unintended request or scheduling constraint in the workload configuration, or ask the platform team to add appropriate capacity. For storage-related failures, follow the volume provisioning runbook. Confirm the pod schedules and becomes Ready; do not remove protective taints or constraints without understanding their purpose.
