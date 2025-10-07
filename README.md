# Sasya Arogya - Platform Engineering

This repository contains the Kubernetes/OpenShift deployment configurations for the Sasya Arogya platform using Kustomize and ArgoCD.

## Architecture Overview

The deployment follows a GitOps approach using ArgoCD with an "App of Apps" pattern and is structured using Kustomize for environment-specific configurations. The platform is deployed across two separate clusters:

- **Development Cluster**: CPU-only workloads for testing and development
- **Production Cluster**: GPU-enabled workloads for live production services

### Components

- **Engine**: Main application backend service
- **Ollama**: AI model serving platform (CPU-only in dev, GPU-enabled in prod)
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
│       ├── engine.yaml           # Engine component
│       ├── ollama.yaml           # Ollama component
│       ├── chromadb.yaml         # ChromaDB component
│       ├── mlflow-tracking.yaml  # MLflow component
│       ├── rag.yaml              # RAG component
│       ├── env-dev.yaml          # Development environment
│       └── env-prod.yaml         # Production environment
├── components/                    # Individual service components
│   ├── engine/base/              # Engine base configuration
│   ├── ollama/base/              # Ollama base configuration (CPU-only)
│   ├── chromadb/base/            # ChromaDB base configuration
│   ├── mlflow-tracking/base/     # MLflow base configuration
│   └── rag/base/                 # RAG base configuration
├── environments/                  # Environment-specific overlays
│   ├── dev/                      # Development environment
│   │   ├── kustomization.yaml   # Dev environment config
│   │   └── patches/              # Dev-specific patches
│   │       ├── engine-dev.yaml
│   │       ├── ollama-dev.yaml  # CPU-only configuration
│   │       ├── chromadb-dev.yaml
│   │       ├── mlflow-dev.yaml
│   │       └── rag-dev.yaml
│   └── prod/                     # Production environment
│       ├── kustomization.yaml   # Prod environment config
│       └── patches/              # Prod-specific patches
│           ├── engine-prod.yaml
│           ├── ollama-prod.yaml # GPU-enabled configuration
│           ├── chromadb-prod.yaml
│           ├── mlflow-prod.yaml
│           └── rag-prod.yaml
├── base/
│   └── common/                   # Common resources (namespace, RBAC)
│       ├── namespace.yaml
│       ├── rbac.yaml
│       └── kustomization.yaml
└── README.md
```

## Environment Architecture

| **Environment** | **Cluster** | **Purpose** | **Resource Profile** | **GPU Support** |
|-----------------|-------------|-------------|---------------------|-----------------|
| **Development** | Dev Cluster | Testing & Development | Low resources, cost-effective | ❌ CPU-only |
| **Production** | Prod Cluster | Live workloads | High resources, HA setup | ✅ GPU-enabled |

## Prerequisites

### For Both Clusters

1. **OpenShift Clusters**: Two separate OpenShift clusters (dev and prod)
2. **ArgoCD Operator**: OpenShift GitOps operator installed on both clusters
3. **Git Repository Access**: Access to this repository from both clusters
4. **Container Registry Access**: Access to quay.io registry
5. **GPU Nodes**: GPU-enabled nodes available in production cluster (for Ollama)

### Cluster-Specific Requirements

**Development Cluster:**
- Minimum 4 CPU cores, 8GB RAM
- Standard storage class available
- No GPU requirements

**Production Cluster:**
- Minimum 16 CPU cores, 32GB RAM
- GPU nodes with NVIDIA drivers
- High-performance storage class
- Load balancer configuration

## Deployment Instructions

### Step 1: Setup ArgoCD (On Both Clusters)

#### Development Cluster
```bash
# Connect to development cluster
oc login <dev-cluster-url>

# Install OpenShift GitOps operator
oc apply -f argocd-install.yaml

# Wait for operator to be ready
oc wait --for=condition=ready pod -l name=argocd-operator -n openshift-gitops-operator --timeout=300s

# Verify ArgoCD installation
oc get pods -n openshift-gitops
```

#### Production Cluster
```bash
# Connect to production cluster
oc login <prod-cluster-url>

# Install OpenShift GitOps operator
oc apply -f argocd-install.yaml

# Wait for operator to be ready
oc wait --for=condition=ready pod -l name=argocd-operator -n openshift-gitops-operator --timeout=300s

# Verify ArgoCD installation
oc get pods -n openshift-gitops
```

### Step 2: Deploy Development Environment

```bash
# Connect to development cluster
oc login <dev-cluster-url>

# Deploy development environment using ArgoCD
oc apply -f argocd/applications/env-dev.yaml

# Verify deployment
oc get applications -n openshift-gitops
oc get deployments -n sasya-arogya
```

**Alternative: Deploy individual components in dev**
```bash
# Deploy components individually (if needed)
oc apply -f argocd/applications/engine.yaml
oc apply -f argocd/applications/ollama.yaml
oc apply -f argocd/applications/chromadb.yaml
oc apply -f argocd/applications/mlflow-tracking.yaml
oc apply -f argocd/applications/rag.yaml
```

### Step 3: Deploy Production Environment

```bash
# Connect to production cluster
oc login <prod-cluster-url>

# Deploy production environment using ArgoCD
oc apply -f argocd/applications/env-prod.yaml

# Verify deployment
oc get applications -n openshift-gitops
oc get deployments -n sasya-arogya

# Check GPU nodes are available for Ollama
oc get nodes -l node.kubernetes.io/instance-type=gpu
```

### Step 4: App-of-Apps Deployment (Alternative Approach)

If you prefer to use the app-of-apps pattern:

```bash
# On the target cluster (dev or prod)
oc apply -f argocd/bootstrap/app-of-apps.yaml

# This will deploy all individual component applications
# You can then sync specific environments as needed
```

## Environment Differences

| **Component** | **Development** | **Production** |
|---------------|-----------------|----------------|
| **Engine** | 1 replica, 2Gi RAM | 3 replicas, 8Gi RAM |
| **Ollama** | 1 replica, CPU-only, 2Gi RAM | 2 replicas, GPU-enabled, 32Gi RAM |
| **ChromaDB** | 1 replica, 1Gi RAM | 3 replicas, 4Gi RAM |
| **MLflow** | 1 replica, 1Gi storage | 2 replicas, 10Gi storage |
| **RAG** | 1 replica, 1Gi RAM | 3 replicas, 4Gi RAM |
| **Total Resources** | ~4 CPU, ~8Gi RAM | ~40+ CPU, ~80+ Gi RAM, 2+ GPUs |

## Kustomize Usage

### Building configurations locally

```bash
# Build development environment
kustomize build environments/dev

# Build production environment
kustomize build environments/prod

# Build individual component
kustomize build components/engine/base

# Validate specific patches
kustomize build environments/dev | grep -A 10 -B 10 "ollama"
```

## Configuration Management

### Adding a New Component

1. **Create component structure:**
   ```bash
   mkdir -p components/new-component/base
   cd components/new-component/base
   ```

2. **Add base resources:**
   - `deployment.yaml`
   - `service.yaml`
   - `route.yaml` (if needed)
   - `kustomization.yaml`

3. **Update environment overlays:**
   ```bash
   # Add to environments/dev/kustomization.yaml
   # Add to environments/prod/kustomization.yaml
   ```

4. **Create environment patches:**
   ```bash
   # Create environments/dev/patches/new-component-dev.yaml
   # Create environments/prod/patches/new-component-prod.yaml
   ```

5. **Create ArgoCD application:**
   ```bash
   # Create argocd/applications/new-component.yaml
   ```

### Updating Images

**Per Environment:**
```yaml
# In environments/dev/kustomization.yaml or environments/prod/kustomization.yaml
images:
  - name: quay.io/rajivranjan/engine
    newTag: amd64-v6  # Update version
```

**Per Component:**
```yaml
# In components/*/base/kustomization.yaml
images:
  - name: quay.io/rajivranjan/engine
    newTag: amd64-v6
```

### Environment Configuration

Environment-specific configurations are managed through patches in the `environments/*/patches/` directories.

**Example: Updating Ollama resources for dev:**
```yaml
# environments/dev/patches/ollama-dev.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ollama
spec:
  template:
    spec:
      containers:
      - name: ollama
        resources:
          requests:
            cpu: '1'      # Increase CPU
            memory: 2Gi   # Increase memory
```

## Monitoring and Troubleshooting

### Access ArgoCD UI

**Development Cluster:**
```bash
oc login <dev-cluster-url>
oc get route openshift-gitops-server -n openshift-gitops
```

**Production Cluster:**
```bash
oc login <prod-cluster-url>
oc get route openshift-gitops-server -n openshift-gitops
```

### Health Checks

**Development Environment:**
```bash
oc login <dev-cluster-url>

# Check all deployments
oc get deployments -n sasya-arogya

# Check specific component
oc get pods -l app=engine -n sasya-arogya

# Check routes
oc get routes -n sasya-arogya

# Check Ollama (CPU-only)
oc logs -l app=ollama -n sasya-arogya
```

**Production Environment:**
```bash
oc login <prod-cluster-url>

# Check all deployments
oc get deployments -n sasya-arogya

# Check GPU allocation for Ollama
oc describe pod -l app=ollama -n sasya-arogya | grep nvidia.com/gpu

# Check routes
oc get routes -n sasya-arogya

# Monitor resource usage
oc top pods -n sasya-arogya
```

### Common Issues

1. **Image pull errors**: 
   - Check image tags and registry access
   - Verify pull secrets if using private registry

2. **Resource limits**: 
   - Adjust resource requests/limits in environment patches
   - Check cluster capacity

3. **GPU scheduling issues** (Production only):
   - Verify GPU nodes are available
   - Check tolerations and node selectors
   - Ensure NVIDIA device plugin is running

4. **Storage issues**: 
   - Verify storage class availability for PVCs
   - Check storage quotas

## Best Practices

### Development Workflow
1. **Local Testing**: Use `kustomize build` to validate changes locally
2. **Dev-First**: Always test changes in development cluster first
3. **Resource Optimization**: Keep dev resources minimal for cost efficiency
4. **CPU Testing**: Test Ollama functionality on CPU before GPU deployment

### Production Deployment
1. **Version Pinning**: Always use specific image tags, never `latest`
2. **Gradual Rollout**: Use rolling updates with health checks
3. **Resource Monitoring**: Monitor GPU and CPU utilization
4. **Backup Strategy**: Ensure persistent volumes are backed up

### Security
1. **RBAC**: Use least privilege access for ArgoCD
2. **Network Policies**: Implement network segmentation
3. **Security Contexts**: Run containers with appropriate security contexts
4. **Image Scanning**: Scan container images for vulnerabilities

## Contributing

1. **Development Flow**:
   ```bash
   # Make changes to components or environments
   git checkout -b feature/new-component
   
   # Test in development
   kustomize build environments/dev
   
   # Deploy to dev cluster
   oc apply -f argocd/applications/env-dev.yaml
   ```

2. **Production Promotion**:
   ```bash
   # After dev validation
   git checkout main
   git merge feature/new-component
   
   # Deploy to production
   oc apply -f argocd/applications/env-prod.yaml
   ```

3. **Documentation**: Update README.md for any architectural changes

## Legacy Structure

The old structure under the `base/` directory (except `base/common/`) is now deprecated. Use the new Kustomize structure for all new deployments and migrations.

## Support

For issues and questions:
1. Check ArgoCD UI for deployment status
2. Review pod logs for application issues
3. Validate Kustomize builds locally
4. Check cluster resources and GPU availability (production)

## Additonal note for system admin

```bash
export OPENAI_API_KEY="sk-your-actual-openai-api-key-here"

kubectl patch secret prescription-secrets \
  --type='json' \
  -p='[{"op": "replace", "path": "/data/openai-api-key", "value":"'$(echo -n "$OPENAI_API_KEY" | base64)'"}]' \
  --namespace=sasya-arogya
  ```