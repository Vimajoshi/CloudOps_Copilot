# Kubernetes Service Unreachable

## Check the service path

Inspect `kubectl -n <namespace> get service <service> -o yaml` and its EndpointSlices. Compare the selector with workload labels, service port with target port, and pod readiness. Test connectivity from an approved pod in the caller's namespace and inspect relevant network policies.

## Repair the verified fault

Correct a mismatched selector or port, recover unhealthy pods, or update an incorrectly scoped network policy through the standard review process. Confirm ready endpoints and repeat the connection test from the caller. Escalate if the underlying cluster network is impaired.
