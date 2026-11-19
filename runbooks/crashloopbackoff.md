# Kubernetes CrashLoopBackOff

## Identify the failing container

Check `kubectl -n <namespace> describe pod <pod>` for container state, restart count, events, and the last termination reason. Inspect `kubectl -n <namespace> logs <pod> -c <container> --previous` for the prior instance's error. Do not paste credentials or sensitive log data into incident tickets.

## Remediate and verify

Match the error to the deployed configuration: correct invalid settings, missing dependencies, or an application startup failure in the deployment source, then roll out the reviewed change. If a recent release caused the failure, consider `kubectl -n <namespace> rollout undo deployment/<deployment>` under the team's rollback policy. Verify `kubectl -n <namespace> rollout status deployment/<deployment>` and confirm restarts stop. Escalate if the cause is unclear; do not repeatedly restart the pod without diagnosis.
