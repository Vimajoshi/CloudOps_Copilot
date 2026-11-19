# Ingress 502 Bad Gateway

## Trace the upstream

For ingress HTTP 502 responses, inspect the ingress controller logs and identify the affected host, path, and backend service. Compare the ingress backend service and port with `kubectl -n <namespace> get service <service> -o yaml` and inspect EndpointSlices and pod readiness. Check application logs and backend connection errors.

## Restore the backend route

Fix a confirmed service selector, target port, ingress route, or unhealthy backend through a reviewed deployment. Check that ready endpoints exist and the application listens on the expected port. Retest the route and monitor 502 rates; avoid exposing an internal service publicly as a workaround.
