# Migration Guide: Old Structure to Kustomize

This guide helps you migrate from the old deployment structure to the new Kustomize-based approach.

## Changes Overview

### Old Structure
```
base/
├── engine/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── route.yaml
├── ollama-both/
├── chromadb-with-data-preloaded/
└── argo-apps/
    └── argo-app-ollama-both.yaml
```

### New Structure
```
components/
├── engine/base/
├── ollama/base/
├── chromadb/base/
environments/
├── dev/
└── prod/
argocd/
├── bootstrap/
└── applications/
```

## Migration Steps

### 1. Update ArgoCD Applications

Replace your current ArgoCD application with the new app-of-apps:

```bash
# Remove old app
oc delete application sasya-arogya-argo-apps-all -n openshift-gitops

# Apply new bootstrap
oc apply -f argocd/bootstrap/app-of-apps.yaml
```

### 2. Environment-Specific Deployment

Choose your deployment approach:

#### Option A: Full Environment (Recommended for new deployments)
```bash
# For development
oc apply -f argocd/applications/env-dev.yaml

# For production
oc apply -f argocd/applications/env-prod.yaml
```

#### Option B: Individual Components (For gradual migration)
```bash
oc apply -f argocd/applications/engine.yaml
oc apply -f argocd/applications/ollama.yaml
oc apply -f argocd/applications/chromadb.yaml
# etc.
```

### 3. Verify Migration

Check that all components are deployed correctly:

```bash
# Check ArgoCD applications
oc get applications -n openshift-gitops

# Check deployments
oc get deployments -n sasya-arogya

# Check services
oc get services -n sasya-arogya

# Check routes
oc get routes -n sasya-arogya
```

## Key Differences

### Service Names
- `ollama-both` → `ollama`
- `chromadb-with-data-amd64` → `chromadb`
- Other services maintain their names

### Resource Management
- **Development**: Reduced resources, no GPU for Ollama
- **Production**: High availability with multiple replicas

### Configuration
- Environment variables now managed through ConfigMaps and patches
- Resource limits properly defined for each environment
- Health checks added for better reliability

## Rollback Plan

If you need to rollback to the old structure:

```bash
# Remove new applications
oc delete application sasya-arogya-app-of-apps -n openshift-gitops

# Reapply old configuration
oc apply -f argo-app.yaml
```

## Validation Checklist

After migration, verify:

- [ ] All ArgoCD applications are synced
- [ ] All pods are running
- [ ] Services are accessible
- [ ] Routes are working
- [ ] Inter-service communication is functional
- [ ] Persistent volumes are mounted correctly

## Troubleshooting

### Common Issues During Migration

1. **Namespace conflicts**: Ensure the `sasya-arogya` namespace exists
2. **RBAC issues**: Verify ArgoCD has proper permissions
3. **Image pull errors**: Check image tags and registry access
4. **Storage class**: Ensure `gp3-csi` storage class is available

### Getting Help

- Check ArgoCD UI for detailed sync status
- Review pod logs: `oc logs <pod-name> -n sasya-arogya`
- Check events: `oc get events -n sasya-arogya --sort-by='.lastTimestamp'`

## Post-Migration Tasks

1. Update CI/CD pipelines to use new image tags
2. Update monitoring configurations
3. Update documentation references
4. Train team on new Kustomize structure
5. Clean up old resources after successful validation
