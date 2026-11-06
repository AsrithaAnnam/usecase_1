# Use Case 07 - Ansible and Vault

## Environment
Windows with WSL Ubuntu, Python virtual environment, and Docker Desktop.
Branch: feature/usecase-07.

## Ansible results
- Inventory targets only localhost.
- Connectivity and Ubuntu facts checks passed.
- Check mode previewed one change.
- First execution reported changed=1 and failed=0.
- Repeat execution reported changed=0 and failed=0.
- Managed file: /tmp/usecase07-managed.conf, permissions 0644.
- Controlled connection failure and localhost recovery were verified.

## Vault results
- Docker development server initialized and unsealed.
- Temporary secret stored at secret/midhlab/app.
- Password read succeeded without displaying its value.
- Repeated writes produced current_version 4, confirming secret versioning.
- The reference guide demonstrates version 2 after exactly two writes.
- No password values or Vault tokens are included in this directory.

## Evidence
Files 01 through 12 under evidence/ record the lab results.
Vault development data is temporary and is lost when its container is removed.
