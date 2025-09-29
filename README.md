# Sasya Chikitsa - Platform Engineering

This repository contains the Kubernetes/OpenShift deployment configurations for the Sasya Chikitsa platform using Kustomize and ArgoCD.

## Architecture Overview

The deployment follows a GitOps approach using ArgoCD with an "App of Apps" pattern and is structured using Kustomize for environment-specific configurations.

### Components

- **Engine**: Main application backend service
- **Ollama**: AI model serving platform
- **ChromaDB**: Vector database for embeddings
- **MLflow Tracking**: ML experiment tracking and model registry
- **RAG**: Retrieval-Augmented Generation service

## Directory Structure

```
platform-engineering/
├── argocd/
│   ├── bootstrap/                 # App of Apps configuration
│   │   └── app-of-apps.yaml      # Bootstrap ArgoCD application
│   └── applications/              # Individual ArgoCD applications
│       ├── engine.yaml
│       ├── ollama.yaml
│       ├── chromadb.yaml
│       ├── mlflow-tracking.yaml
│       ├── rag.yaml
│       ├── env-dev.yaml          # Development environment
│       └── env-prod.yaml         # Production environment
├── components/                    # Individual service components
│   ├── engine/
│   │   └── base/
│   │       ├── deployment.yaml
│   │       ├── service.yaml
│   │       ├── route.yaml
│   │       └── kustomization.yaml
│   ├── ollama/
│   ├── chromadb/
│   ├── mlflow-tracking/
│   └── rag/
├── environments/                  # Environment-specific overlays
│   ├── dev/
│   │   ├── kustomization.yaml
│   │   └── patches/              # Environment-specific patches
│   │       ├── engine-dev.yaml
│   │       └── ...
│   └── prod/
│       ├── kustomization.yaml
│       └── patches/
├── base/
│   └── common/                   # Common resources (namespace, RBAC)
│       ├── namespace.yaml
│       ├── rbac.yaml
│       └── kustomization.yaml
└── README.md
```

## Deployment Instructions

### Prerequisites

1. OpenShift cluster with ArgoCD operator installed
2. Git repository access
3. Container registry access (quay.io)

### Setup ArgoCD

1. Install the OpenShift GitOps operator:
   ```bash
   oc apply -f argocd-install.yaml
   ```

2. Deploy the app-of-apps:
   ```bash
   oc apply -f argocd/bootstrap/app-of-apps.yaml
   ```

### Environment Deployment

#### Development Environment
```bash
# Deploy development environment
oc apply -f argocd/applications/env-dev.yaml
```

#### Production Environment
```bash
# Deploy production environment
oc apply -f argocd/applications/env-prod.yaml
```

#### Individual Components
You can also deploy individual components:
```bash
oc apply -f argocd/applications/engine.yaml
oc apply -f argocd/applications/ollama.yaml
# etc.
```

## Kustomize Usage

### Building configurations locally

```bash
# Build development environment
kustomize build environments/dev

# Build production environment
kustomize build environments/prod

# Build individual component
kustomize build components/engine/base
```

### Environment Differences

| Component | Dev | Prod |
|-----------|-----|------|
| Engine | 1 replica, 2Gi RAM | 3 replicas, 8Gi RAM |
| Ollama | 1 replica, no GPU | 2 replicas, GPU enabled |
| ChromaDB | 1 replica, 1Gi RAM | 3 replicas, 4Gi RAM |
| MLflow | 1 replica, 2Gi RAM | 2 replicas, 8Gi RAM |
| RAG | 1 replica, 1Gi RAM | 3 replicas, 4Gi RAM |

## Configuration Management

### Adding a New Component

1. Create component directory structure:
   ```bash
   mkdir -p components/new-component/base
   ```

2. Add base resources (deployment, service, route, kustomization.yaml)

3. Update environment overlays in `environments/*/kustomization.yaml`

4. Create ArgoCD application in `argocd/applications/`

### Updating Images

Images can be updated in several ways:

1. **Environment-specific**: Update `images` section in `environments/*/kustomization.yaml`
2. **Component-specific**: Update `images` section in `components/*/base/kustomization.yaml`
3. **ArgoCD**: Update `kustomize.images` in ArgoCD application manifests

### Environment Configuration

Environment-specific configurations are managed through patches in the `environments/*/patches/` directories.

## Monitoring and Troubleshooting

### ArgoCD UI

Access ArgoCD UI to monitor deployments:
```bash
# Get ArgoCD route
oc get route openshift-gitops-server -n openshift-gitops
```

### Checking Deployments

```bash
# Check all deployments
oc get deployments -n sasya-arogya

# Check specific component
oc get pods -l app=engine -n sasya-arogya

# Check routes
oc get routes -n sasya-arogya
```

### Common Issues

1. **Image pull errors**: Check image tags and registry access
2. **Resource limits**: Adjust resource requests/limits in patches
3. **Storage issues**: Verify storage class availability for PVCs

## Best Practices

1. **Version Control**: Always tag releases and use specific image tags
2. **Environment Promotion**: Use same image tags across environments
3. **Resource Management**: Set appropriate resource limits for each environment
4. **Security**: Use least privilege RBAC and security contexts
5. **Monitoring**: Implement health checks and monitoring for all components

## Contributing

1. Make changes to component base configurations
2. Test in development environment first
3. Update documentation as needed
4. Create pull request for review
5. Promote to production after validation

## Legacy Structure

The old structure under the `base/` directory (except `base/common/`) is now deprecated. Use the new Kustomize structure for all new deployments and migrations.