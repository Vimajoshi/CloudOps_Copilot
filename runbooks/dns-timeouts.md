# Kubernetes DNS Timeouts

## Isolate DNS failure

From an approved diagnostic pod, resolve the affected service's fully qualified name and compare it with a known working name. Check `kubectl -n kube-system get pods -l k8s-app=kube-dns`, DNS service endpoints, CoreDNS logs, and network policies. Identify whether the failure affects one namespace, the cluster, or upstream DNS.

## Restore name resolution

Correct a verified service name, missing endpoint, network policy, or upstream resolver issue through the normal change process. If CoreDNS is unhealthy, inspect its configuration and capacity before a controlled rollout or scale change. Retry resolution from an affected workload and monitor DNS error rates.
