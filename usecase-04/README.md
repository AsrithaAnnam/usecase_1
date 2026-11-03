\# Use Case 04 - Deploy the Claims App to Kubernetes



\## Environment



\- Branch: feature/usecase-4-kubernetes

\- Cluster: Docker Desktop Kubernetes

\- Namespace: claims-k8s-lab

\- Registry: registry.gitlab.com/asrithaannam/usecase\_1

\- Application deployment: raw Kubernetes YAML

\- Ingress controller: Traefik, installed using Helm



\## Components



\- React frontend with Nginx on port 8080

\- Flask backend with Gunicorn on port 5000

\- PostgreSQL 16 with a 1 Gi persistent volume

\- ConfigMap for database settings

\- Separate Secrets for database and registry credentials

\- Readiness and liveness probes

\- Ingress routing / to the frontend and /api to the backend



The frontend Nginx configuration also proxies /api to backend:5000.



\## Deployment



Create the namespace first:



```cmd

kubectl apply -f usecase-04\\k8s\\namespace.yaml

```



Before deploying the remaining resources, create these Secrets locally:



\- claims-db-secret: key DB\_PASSWORD

\- gitlab-pull-secret: GitLab registry authentication



Credentials are not stored in Git.



Install the Ingress controller:



```cmd

helm repo add traefik https://traefik.github.io/charts

helm upgrade --install traefik traefik/traefik --namespace traefik --create-namespace --set service.type=ClusterIP --wait --timeout 180s

```



Apply the application manifests:



```cmd

kubectl apply -f usecase-04\\k8s\\

```



The database initialization script runs only when PostgreSQL initializes an empty data directory.



\## Access



```cmd

kubectl port-forward -n traefik service/traefik 8090:80

```



Keep the terminal running and open http://localhost:8090.



\## Validation Completed



\- All three Deployments available with Ready pods.

\- Database PVC Bound.

\- users and claims tables verified.

\- Application loaded through Ingress.

\- /api/claims returned HTTP 200 with database records.

\- Backend startup logs reviewed.

\- Invalid readiness path caused the test rollout to time out.

\- kubectl rollout undo restored the backend.

\- Health endpoint returned healthy after recovery.

\- All 11 manifests passed server-side dry-run validation.



\## Differences from the Reference PDF



\- GitLab Container Registry replaces Harbor.

\- Backend port is 5000.

\- Traefik replaces the retired ingress-nginx controller.

\- Kubernetes backend Service is named backend to match Nginx configuration.

