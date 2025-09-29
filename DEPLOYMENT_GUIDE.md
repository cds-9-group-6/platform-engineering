# Quick Deployment Guide - Sasya Arogya

This guide provides the essential commands for deploying Sasya Arogya across dev and prod clusters.

## Prerequisites Checklist

- [ ] Two OpenShift clusters (dev and prod) are accessible
- [ ] ArgoCD operator installed on both clusters
- [ ] Production cluster has GPU nodes available
- [ ] Registry access configured (quay.io)

## Deployment Commands

### 🚀 Development Cluster Deployment

```bash
# 1. Connect to development cluster
oc login <dev-cluster-url>

# 2. Install ArgoCD (if not done)
oc apply -f argocd-install.yaml

# 3. Deploy development environment
oc apply -f argocd/applications/env-dev.yaml

# 4. Verify deployment
oc get applications -n openshift-gitops
oc get deployments -n sasya-arogya
oc get routes -n sasya-arogya
```

### 🏭 Production Cluster Deployment

```bash
# 1. Connect to production cluster
oc login <prod-cluster-url>

# 2. Install ArgoCD (if not done)
oc apply -f argocd-install.yaml

# 3. Deploy production environment
oc apply -f argocd/applications/env-prod.yaml

# 4. Verify deployment
oc get applications -n openshift-gitops
oc get deployments -n sasya-arogya
oc get routes -n sasya-arogya

# 5. Check GPU allocation (Ollama)
oc describe pod -l app=ollama -n sasya-arogya | grep nvidia.com/gpu
```

## Resource Overview

| Environment | Cluster | CPU | Memory | GPU | Storage |
|------------|---------|-----|--------|-----|---------|
| **Dev** | Dev Cluster | ~4 cores | ~8Gi | None | ~5Gi |
| **Prod** | Prod Cluster | ~40+ cores | ~80+ Gi | 2+ GPUs | ~25Gi |

## Access URLs

After deployment, get the routes:

```bash
# Development
oc login <dev-cluster-url>
oc get routes -n sasya-arogya

# Production  
oc login <prod-cluster-url>
oc get routes -n sasya-arogya
```

## ArgoCD UI Access

```bash
# Development ArgoCD
oc login <dev-cluster-url>
echo "Dev ArgoCD: $(oc get route openshift-gitops-server -n openshift-gitops -o jsonpath='{.spec.host}')"

# Production ArgoCD
oc login <prod-cluster-url>
echo "Prod ArgoCD: $(oc get route openshift-gitops-server -n openshift-gitops -o jsonpath='{.spec.host}')"
```

## Common Troubleshooting

### Development Issues
```bash
# Check pod logs
oc logs -l app=<component> -n sasya-arogya

# Check resource constraints
oc describe pods -n sasya-arogya

# Restart failing deployment
oc rollout restart deployment/<component> -n sasya-arogya
```

### Production Issues
```bash
# Check GPU availability
oc get nodes -l node.kubernetes.io/instance-type=gpu
oc describe node <gpu-node-name>

# Check Ollama GPU allocation
oc describe pod -l app=ollama -n sasya-arogya

# Monitor resource usage
oc top pods -n sasya-arogya
oc top nodes
```

## Quick Updates

### Update Image Tag
```bash
# Edit the appropriate environment kustomization
vim environments/dev/kustomization.yaml   # for dev
vim environments/prod/kustomization.yaml  # for prod

# Update the image tag in the images section
# ArgoCD will auto-sync if configured
```

### Force Sync
```bash
# If auto-sync is disabled, manually sync via ArgoCD UI or:
oc patch application <app-name> -n openshift-gitops --type merge -p '{"operation":{"sync":{"syncStrategy":{"hook":{"force":true}}}}}'
```

## Support

- 📖 Full documentation: [README.md](README.md)
- 🔄 Migration guide: [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
- 🎯 ArgoCD UI: Check routes above
- 📊 Component health: Monitor via ArgoCD applications
