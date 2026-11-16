\# Use Case 13 Policy Balance



\## Policy objective



Each container in the Deployment must specify CPU and memory requests

and limits. Conftest checks these fields before deployment.



\## Risk prevented



Requests help Kubernetes schedule Pods. Limits reduce the risk that one

container uses resources needed by other workloads.



\## Why this rule is practical



Each application team can choose resource values that fit its workload.

If a field is missing, Conftest names the container and the field to add.



\## Result



\- The unsafe manifest failed with four missing resource fields.

\- Kubernetes confirmed the unsafe Deployment was absent.

\- The corrected manifest passed all four policy checks and rolled out.

\- The Pod was 1/1 Running, and nginx returned HTTP 200 OK.
