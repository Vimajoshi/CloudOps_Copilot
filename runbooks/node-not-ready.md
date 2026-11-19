# Kubernetes NodeNotReady

## Inspect node condition

Run `kubectl get nodes` and `kubectl describe node <node>`. Inspect Ready condition, memory and disk pressure, kubelet connectivity, recent events, and affected workloads. Check the cloud provider's instance and network health before assuming the node is faulty.

## Recover node capacity

Escalate to the platform team if the kubelet or underlying instance is unhealthy. Follow the approved node replacement procedure and account for workload disruption budgets and capacity before draining a node. Confirm replacement capacity joins Ready and affected pods become healthy; investigate the underlying disk, memory, or networking cause.
