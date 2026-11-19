# Database Connection Exhaustion

## Diagnose exhausted connections

Confirm connection-limit errors in application and database metrics, then compare active and idle sessions, pool sizes, connection limits, traffic, and recent deployments. Check for slow queries and connection leaks. Avoid logging connection strings or credentials.

## Reduce pressure safely

Ask the database owner to assess slow sessions and connection pool limits. Correct a confirmed leak or excessive pool setting, or carefully scale application traffic and capacity according to the team's change process. Avoid terminating database sessions or increasing the server limit without evaluating impact. Verify connection counts and error rate recover.
