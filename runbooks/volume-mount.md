# Persistent Volume Mount Failures

## Identify the storage failure

Inspect pod Events using `kubectl -n <namespace> describe pod <pod>` and inspect the PVC with `kubectl -n <namespace> describe pvc <claim>`. Determine whether the claim is Pending, attachment is blocked, permissions fail, or the storage backend is unavailable. Check the StorageClass and CSI driver health with the platform team.

## Restore volume access

Correct the confirmed StorageClass, zone, or access-mode mismatch via the approved infrastructure process, or restore the storage backend. Do not delete a PVC or persistent volume as a troubleshooting step: this can destroy data. Verify the claim is Bound, the mount succeeds, and the application can safely read its data.
