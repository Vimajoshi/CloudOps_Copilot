# Kubernetes ImagePullBackOff

## Diagnose image pull failures

Run `kubectl -n <namespace> describe pod <pod>` and inspect Events for `ImagePullBackOff`, `ErrImagePull`, registry authentication, missing image, or network errors. Compare the image name, tag, registry address, and image pull secret reference with the intended release; never copy credentials into a ticket.

## Restore image access

Correct an invalid image reference in the deployment, or have the registry owner repair the relevant pull permissions or secret. For network failures, check registry reachability and approved egress rules with the platform team. Apply the reviewed change and check `kubectl -n <namespace> rollout status deployment/<deployment>` and pod events.
