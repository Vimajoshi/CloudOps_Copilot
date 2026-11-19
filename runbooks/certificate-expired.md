# Expired TLS Certificate

## Confirm certificate and scope

Inspect the certificate presented by the affected hostname and its expiration date using an approved TLS inspection tool. Check the relevant ingress or load balancer certificate configuration and renewal controller status. Distinguish expiration from a hostname mismatch or trust-chain failure.

## Renew and verify

Follow the certificate owner's approved renewal and secret rotation procedure; never include private keys in logs or tickets. Verify the new certificate is served for the correct hostname, has the intended chain and expiration, and is accepted by a client. Check renewal alerts and controller health.
