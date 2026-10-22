# Use Case 2: Kubernetes Deployment, Promotion, and Helm Rollback

## 1. Project Overview

This project deploys a three-tier Claims Management Application to Kubernetes using Helm.

The application contains:

| Component | Technology | Responsibility |
|---|---|---|
| Frontend | React served by Nginx | Displays the application in the browser |
| Backend | Python Flask | Processes API requests |
| Database | PostgreSQL | Stores users and claims |

Use Case 2 reuses the frontend and backend container images from Use Case 1. These images are deployed to three Kubernetes namespaces without rebuilding them.

## 2. What This Use Case Demonstrates

- Deploying a three-tier application using a Helm chart.
- Reusing container images by their SHA-256 digests.
- Promoting the same application version through Dev, Stage, and Prod-like.
- Keeping database storage separate for each environment.
- Configuring private registry access using Kubernetes Secrets.
- Recording a simulated manual approval.
- Simulating a release with an invalid backend image.
- Restoring the working application using Helm rollback.
- Verifying the application after recovery.

This is a local training environment. Prod-like represents a practice environment that resembles production; it does not serve real customers.

## 3. Application Architecture

Within each namespace, requests follow this path:

1. The browser connects to the frontend through a local port-forward.
2. Nginx serves the React application.
3. Requests beginning with `/api/` are forwarded to the backend Service.
4. The Flask backend reads or writes data in PostgreSQL.
5. The response returns to the browser.

| Kubernetes Service | Port | Purpose |
|---|---|---|
| frontend | 80 | Serves the application |
| backend | 5000 | Handles API requests |
| database | 5432 | Accepts PostgreSQL connections |

The frontend Nginx configuration uses:

```nginx
location /api/ {
    proxy_pass http://backend:5000/api/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

The name `backend` resolves to the backend Service in the same namespace.

## 4. Environments

| Namespace | Purpose | Local browser address |
|---|---|---|
| dev | First deployment and application testing | http://localhost:8081 |
| stage | Validation before the final lab deployment | http://localhost:8082 |
| prod-like | Simulated approval, failure, and rollback | http://localhost:8083 |

Each namespace has its own frontend, backend, database, Secrets, and database storage.

### Why records differ between environments

Records belong to a database, not a browser port.

A claim created in Dev does not automatically appear in Stage or Prod-like because each environment uses a separate database.

The earlier Use Case 1 application on port 8080 also uses separate database storage.

We promote application versions between environments. We do not copy database records.

## 5. Prerequisites

Before deployment, ensure that:

- Git, Docker, kubectl, and Helm are installed.
- Docker is running when required by the local Kubernetes setup.
- A Kubernetes cluster is running and accessible.
- The cluster has a default StorageClass for the database PVC.
- The frontend and backend images exist in GitLab Container Registry.
- A GitLab credential with permission to pull the images is available.

Run commands from the project root in Windows Command Prompt:

```bat
cd C:\Users\Dell\Desktop\3-Tier-Architecture
```

Check the tools and cluster:

```bat
git --version
docker version
kubectl version --client
helm version
kubectl config current-context
kubectl get nodes
kubectl get storageclass
```

Confirm that the selected Kubernetes context is the intended lab cluster.

## 6. Feature Branch

The implementation is stored on:

```text
feature/usecase-2-helm-rollback
```

To switch to the existing branch:

```bat
git switch feature/usecase-2-helm-rollback
```

When starting a new implementation from the intended Use Case 1 base branch, create the feature branch with:

```bat
git switch -c feature/usecase-2-helm-rollback
```

Create the branch only once.

## 7. Helm Chart Structure

The deployment files are under `claims-app/`:

```text
claims-app/
    .helmignore
    Chart.yaml
    values.yaml
    files/
        init.sql
    templates/
        _helpers.tpl
        backend.yaml
        frontend.yaml
        database.yaml
```

| File | Purpose |
|---|---|
| Chart.yaml | Describes the Helm chart |
| values.yaml | Stores image references and deployment settings |
| files/init.sql | Contains the database initialization script |
| templates/backend.yaml | Creates the backend Deployment and Service |
| templates/frontend.yaml | Creates the frontend Deployment and Service |
| templates/database.yaml | Creates the database resources and storage |
| templates/_helpers.tpl | Contains generated reusable template helpers |
| .helmignore | Defines files excluded from chart packaging |

### Commands used to create the chart

These commands document the original setup. Do not rerun the template deletion commands against the completed chart.

```bat
helm create claims-app
dir claims-app\templates
del claims-app\templates\*.yaml
rmdir /s /q claims-app\templates\tests
del claims-app\templates\NOTES.txt
mkdir claims-app\files
copy database\init.sql claims-app\files\init.sql
```

The generated starter templates were replaced with templates for this application.

## 8. Image Configuration

The application images are selected by digest in `claims-app/values.yaml`:

```yaml
imagePullSecrets:
  - name: gitlab-registry

backend:
  repository: registry.gitlab.com/asrithaannam/usecase_1/backend
  digest: sha256:9475d75b0e0a2e69ca16bc4b9e824517ca087cf92adad05bc4f283b3b1e84c90
  replicas: 1
  port: 5000

frontend:
  repository: registry.gitlab.com/asrithaannam/usecase_1/frontend
  digest: sha256:cc841773f8da08f77ab9474e3ee22e7a4d5d990aeb14fc16173d5ec1078f0ead
  replicas: 1
  port: 80

database:
  image: postgres:17-alpine
  name: claimsdb
  username: claimsuser
  existingSecret: claims-db-secret
  storage: 1Gi
```

A digest identifies specific image content. Using the same frontend and backend digests keeps the application image versions consistent across environments.

The PostgreSQL image uses a tag in this lab. It is not pinned by digest in the chart.

## 9. Validate the Chart

```bat
helm lint claims-app
```

Expected result:

```text
1 chart(s) linted, 0 chart(s) failed
```

The message `Chart.yaml: icon is recommended` is informational.

Linting checks the chart structure and rendering. It does not prove that images can be pulled or that the application works.

## 10. Create the Namespaces

For a fresh setup:

```bat
kubectl create namespace dev
kubectl create namespace stage
kubectl create namespace prod-like
kubectl get namespaces
```

If the namespaces already exist, continue using them.

## 11. Configure GitLab Registry Access

Kubernetes needs its own registry credentials. Logging in with Docker alone does not configure Kubernetes image pulls.

Replace `YOUR_GITLAB_TOKEN` with a credential that has permission to pull the images.

Run these commands locally. Do not commit the token or include it in screenshots.

```bat
kubectl create secret docker-registry gitlab-registry --docker-server=registry.gitlab.com --docker-username=asrithaannam --docker-password="YOUR_GITLAB_TOKEN" -n dev

kubectl create secret docker-registry gitlab-registry --docker-server=registry.gitlab.com --docker-username=asrithaannam --docker-password="YOUR_GITLAB_TOKEN" -n stage

kubectl create secret docker-registry gitlab-registry --docker-server=registry.gitlab.com --docker-username=asrithaannam --docker-password="YOUR_GITLAB_TOKEN" -n prod-like
```

Each namespace needs its own Secret because Secrets are namespace-scoped.

These creation commands are for a fresh setup. They return an AlreadyExists error if the Secrets are already present.

## 12. Configure the Database Password

Replace `YOUR_DB_PASSWORD` with a database password chosen for the lab.

The original exercise used the same password value in all three namespaces. The databases remain separate.

```bat
kubectl create secret generic claims-db-secret --from-literal=password="YOUR_DB_PASSWORD" -n dev

kubectl create secret generic claims-db-secret --from-literal=password="YOUR_DB_PASSWORD" -n stage

kubectl create secret generic claims-db-secret --from-literal=password="YOUR_DB_PASSWORD" -n prod-like
```

The backend and PostgreSQL read the password from the Secret named `claims-db-secret`.

Do not store real passwords in `values.yaml` or Git.

## 13. Database Initialization and Storage

The database template creates:

- A ConfigMap containing `init.sql`.
- A PersistentVolumeClaim named `database-data`.
- A Service named `database`.
- A PostgreSQL Deployment.

PostgreSQL runs the initialization script when it initializes an empty data directory.

Restarting a database Pod with existing data does not rerun the initialization script.

The PVC allows database files to survive Pod replacement. It is not a database backup.

## 14. Deploy to Dev

```bat
helm install claims-app claims-app -n dev --wait --timeout 5m
```

In this command:

- The first `claims-app` is the Helm release name.
- The second `claims-app` is the chart directory.
- `-n dev` selects the namespace.
- `--wait` waits for supported resources to become ready.
- `--timeout 5m` sets the waiting limit.

Check the Pods:

```bat
kubectl get pods -n dev
```

Expected result: backend, frontend, and database each show `1/1 Running`.

Check the deployed application image references:

```bat
kubectl get deployments backend frontend -n dev -o custom-columns="NAME:.metadata.name,IMAGE:.spec.template.spec.containers[0].image"
```

Check the image IDs reported by running containers:

```bat
kubectl get pods -n dev -o custom-columns="POD:.metadata.name,IMAGE_ID:.status.containerStatuses[0].imageID"
```

For multi-platform images, a runtime may report a platform-specific digest rather than the image index digest.

## 15. Test Dev

```bat
kubectl port-forward -n dev service/frontend 8081:80
```

Open:

```text
http://localhost:8081
```

Create a test claim and confirm that it appears in the list.

Port 8080 was already occupied during the exercise, so port 8081 was used.

Press `Ctrl+C` to stop port-forwarding before entering more commands in the same terminal.

Stopping port-forwarding does not stop the Kubernetes application.

## 16. Promote to Stage

Deploy the same chart and application image digests:

```bat
helm install claims-app claims-app -n stage --wait --timeout 5m
```

Verify:

```bat
kubectl get pods -n stage
kubectl get deployments backend frontend -n stage -o custom-columns="NAME:.metadata.name,IMAGE:.spec.template.spec.containers[0].image"
```

Test Stage:

```bat
kubectl port-forward -n stage service/frontend 8082:80
```

Open:

```text
http://localhost:8082
```

Create a claim and confirm it appears.

Stage has a separate database, so Dev records are not expected to appear.

Press `Ctrl+C` when finished.

## 17. Deploy to Prod-like with Simulated Approval

After successful Stage testing:

```bat
helm install claims-app claims-app -n prod-like --wait --timeout 5m --description "Manual lab approval recorded after successful Stage validation"
```

The description records the simulated approval in Helm history.

This is a manual lab convention. It does not enforce an approval gate or prevent someone from deploying.

Verify:

```bat
kubectl get pods -n prod-like
kubectl get deployments backend frontend -n prod-like -o custom-columns="NAME:.metadata.name,IMAGE:.spec.template.spec.containers[0].image"
```

## 18. Test Prod-like

```bat
kubectl port-forward -n prod-like service/frontend 8083:80
```

Open:

```text
http://localhost:8083
http://localhost:8083/api/health
```

Create a test claim and confirm it appears in the list.

The health endpoint should return a healthy response.

Press `Ctrl+C` when finished.

## 19. Simulate a Bad Backend Release

Run this only in the lab Prod-like namespace.

The following command changes the release to reference a nonexistent backend digest:

```bat
helm upgrade claims-app claims-app -n prod-like --reuse-values --set backend.digest=sha256:0000000000000000000000000000000000000000000000000000000000000000 --description "Lab failure simulation using nonexistent backend image digest"
```

This creates Helm revision 2 in the original exercise.

The command deliberately omits `--wait`, allowing the failed rollout to be inspected.

It changes the Helm release values; it does not edit the local `values.yaml` file.

## 20. Inspect the Failed Rollout

```bat
kubectl get pods -n prod-like
helm history claims-app -n prod-like
```

The new backend Pod should show `ErrImagePull` or `ImagePullBackOff`.

To inspect the cause, replace `FAILED_BACKEND_POD_NAME` with the actual Pod name:

```bat
kubectl describe pod FAILED_BACKEND_POD_NAME -n prod-like
```

During the completed exercise:

- The new backend Pod could not pull the nonexistent image.
- The previous healthy backend Pod remained running.
- Helm showed revision 2 as deployed because the upgrade did not wait for readiness.

This demonstrated a failed rollout. It did not demonstrate a complete application outage.

## 21. Roll Back to the Working Release

In the original exercise, revision 1 was the known-good release:

```bat
helm rollback claims-app 1 -n prod-like --wait --timeout 5m
```

Expected output:

```text
Rollback was a success! Happy Helming!
```

Helm creates a new revision for the rollback. It does not erase the earlier revisions.

## 22. Verify Recovery

```bat
kubectl get pods -n prod-like
helm history claims-app -n prod-like
kubectl get deployment backend -n prod-like -o custom-columns="NAME:.metadata.name,IMAGE:.spec.template.spec.containers[0].image"
```

The original exercise produced:

| Revision | Description | Status after rollback |
|---|---|---|
| 1 | Manual lab approval recorded after successful Stage validation | superseded |
| 2 | Lab failure simulation using nonexistent backend image digest | superseded |
| 3 | Rollback to 1 | deployed |

The restored backend digest is:

```text
sha256:9475d75b0e0a2e69ca16bc4b9e824517ca087cf92adad05bc4f283b3b1e84c90
```

If the exercise is repeated, revision numbers will increase. Check Helm history before selecting a rollback target.

## 23. Verify the Application After Rollback

```bat
kubectl port-forward -n prod-like service/frontend 8083:80
```

Open:

```text
http://localhost:8083/api/health
http://localhost:8083
```

Confirm that:

- The health endpoint responds successfully.
- The earlier claim remains in the list.
- A new claim can be created.

A new claim was successfully created after rollback during the completed exercise.

### What rollback means for the database

Helm rollback restores the earlier release configuration.

It does not restore a database backup, undo SQL changes, or copy records between environments.

In this exercise, the database continued using its existing PVC.

Press `Ctrl+C` when testing is complete.

## 24. Commit and Push the Chart

The chart was committed using:

```bat
git branch --show-current
git status --short
git add claims-app
git commit -m "Add Helm chart for three-tier promotion and rollback lab"
git push github feature/usecase-2-helm-rollback
```

The chart implementation commit is:

```text
ab08a92
```

The remote name `github` refers to this repository's configured Git remote.

Check configured remotes with:

```bat
git remote -v
```

The generated `.coverage` file was left untracked and was not included in the chart commit.

## 25. Troubleshooting

| Issue | Meaning | Action |
|---|---|---|
| Local port 8080 is occupied | Another process is listening on that port | Use the documented alternative port |
| `helm` is not recognized | Helm is unavailable in the terminal's PATH | Open a fresh terminal and check `helm version` |
| LF-to-CRLF warning from Git | Git is reporting line-ending conversion | Review normally; this warning did not block the commit |
| `ImagePullBackOff` | Kubernetes cannot pull the image | Check the image reference, registry access, and Pod events |
| PVC remains Pending | Storage has not been provisioned | Check the StorageClass and PVC events |
| Records differ across environments | Each environment uses a separate database | This is expected |
| Helm says deployed but a Pod is unhealthy | Release submission did not establish application health | Inspect Pods, rollout status, and events |
| `helm install` says the release name is in use | A release already exists in that namespace | Inspect the release before choosing an upgrade |
| Previous failed Pod is gone after rollback | Kubernetes removed it while reconciling the restored Deployment | Use previously captured evidence for its earlier error |

## 26. Demonstration Evidence

Useful screenshots include:

1. Ready Pods in Dev, Stage, and Prod-like.
2. Helm history showing simulated approval, the bad release, and rollback.
3. Restored frontend and backend image digests.
4. The working claims list after rollback.
5. The healthy API response.

The failed Pod screenshot must be captured while the failure is present. Helm history alone does not prove the Pod's exact error.

## 27. Completed Outcome

The exercise successfully demonstrated:

- Reuse of Use Case 1 application images without rebuilding.
- Deployment to Dev, Stage, and Prod-like using Helm.
- Independent database storage in each namespace.
- Simulated manual approval recorded in release history.
- A deliberately failed backend image rollout.
- Rollback to the known-good release configuration.
- Successful application use after recovery.
- Helm chart commit and push to GitHub.

Branch:

[feature/usecase-2-helm-rollback](https://github.com/AsrithaAnnam/usecase_1/tree/feature/usecase-2-helm-rollback)