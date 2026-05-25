---
name: skill-devops
description: Infrastructure-as-code, containerization, orchestration, and platform engineering for web applications. Use when writing Dockerfiles, designing Kubernetes manifests, provisioning cloud infrastructure with Terraform/Pulumi, managing secrets, or building developer platforms. NOT for release strategies or deployment pipelines — that's skill-deployment.
---

# DevOps — Infrastructure & Platform

This skill owns *what runs the application*. The pipelines and release strategies that put code on top of it belong to `skill-deployment`.

## When to Activate

Use when:
- Writing or reviewing a Dockerfile
- Designing Docker Compose stacks for local or shared dev
- Authoring Kubernetes manifests (Deployment, Service, Ingress, HPA)
- Defining infrastructure as code (Terraform, Pulumi, CDK, Bicep)
- Managing secrets (Vault, AWS Secrets Manager, sealed-secrets)
- Choosing between cloud platforms or sizing instances
- Setting up developer platforms (internal CLIs, golden paths)

## When NOT to Use

| Situation | Use instead |
|---|---|
| Designing the CI/CD pipeline that uses this infra | `skill-deployment` |
| Writing the application code that runs in the container | `skill-backend` / `skill-frontend` |
| Wiring up tracing, metrics, and dashboards | `skill-observability` |
| Implementing auth on top of the infra | `skill-auth` |
| Hardening secrets, network policy, IAM | `shared/skill-security` |

## Iron Laws

1. **Infrastructure changes go through code review** — no console clicks in production.
2. **Containers are immutable** — config goes in env vars or mounted volumes, never baked-in secrets.
3. **The Dockerfile must be reproducible** — same input, same image. Pin every base, every dep, every binary.

## Containerization

### Dockerfile — multi-stage, pinned, non-root

```dockerfile
# syntax=docker/dockerfile:1.7
FROM node:20.11.1-alpine3.19 AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci

FROM node:20.11.1-alpine3.19 AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:20.11.1-alpine3.19 AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup -S app && adduser -S app -G app
USER app
COPY --from=builder --chown=app:app /app/dist ./dist
COPY --from=builder --chown=app:app /app/node_modules ./node_modules
COPY --from=builder --chown=app:app /app/package.json ./
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1
CMD ["node", "dist/index.js"]
```

What this enforces: pinned base image (Alpine version included), separate dep / build / runtime layers, non-root user, healthcheck, BuildKit cache mount for fast rebuilds.

Common mistakes to avoid:
- `FROM node:latest` — non-reproducible, surprises on the next pull
- `COPY . .` before `npm ci` — busts the cache on every code change
- Running as root — container breakout becomes host root
- No `HEALTHCHECK` — orchestrator can't tell if the app is wedged

### Docker Compose — for local dev only

```yaml
services:
  app:
    build:
      context: .
      target: builder    # use the dev-friendly stage
    ports: ["3000:3000"]
    volumes:
      - .:/app
      - /app/node_modules    # don't shadow with host dir
    environment:
      DATABASE_URL: postgres://app:devpw@db:5432/app
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16.2-alpine
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: devpw
      POSTGRES_DB: app
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 5s
      retries: 10

volumes:
  db_data:
```

Compose is for local/dev, not prod. Use Kubernetes, ECS, or a managed platform for production.

## Kubernetes Essentials

A minimum viable production workload needs four resources: Deployment, Service, Ingress, and a way to set config.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: api, labels: { app: api } }
spec:
  replicas: 3
  selector: { matchLabels: { app: api } }
  template:
    metadata: { labels: { app: api } }
    spec:
      containers:
        - name: api
          image: registry.example.com/api:1.4.2
          ports: [{ containerPort: 3000 }]
          env:
            - name: DATABASE_URL
              valueFrom: { secretKeyRef: { name: api-secrets, key: db-url } }
          resources:
            requests: { cpu: 100m, memory: 128Mi }
            limits:   { cpu: 500m, memory: 512Mi }
          livenessProbe:
            httpGet: { path: /health, port: 3000 }
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet: { path: /ready, port: 3000 }
            periodSeconds: 5
```

What to always set:
- **Resource requests AND limits** — without limits, one bad replica eats the node
- **Liveness AND readiness probes** — they answer different questions ("kill me" vs "send me traffic")
- **Pinned image tag** — never `:latest` in K8s, ever
- **Secrets via `secretKeyRef`** — never inline in env

## Infrastructure as Code

| Tool | Strength | Use when |
|---|---|---|
| Terraform | Mature, multi-cloud, huge provider ecosystem | Default for cloud infra |
| Pulumi | Real programming language | Complex logic, type safety matters |
| AWS CDK | Native AWS, TypeScript/Python | All-in on AWS |
| Bicep | Native Azure | All-in on Azure |
| Crossplane | K8s-native | You already run K8s and want to manage infra from it |

Discipline (regardless of tool):
- **State lives in remote backend** with locking — never local, never unencrypted
- **Plan reviewed before apply** — every change shows up as a diff in PR
- **Modules for repeated patterns** — VPC, IAM role, queue + DLQ, etc.
- **No drift tolerance** — if console changes happen, reconcile or revert

## Secrets Management

Three rules:
1. Never commit a secret. Pre-commit hooks (`gitleaks`, `trufflehog`) are mandatory.
2. Never bake secrets into images. Inject at runtime.
3. Rotate on a schedule and on every personnel change.

| Tool | Best for |
|---|---|
| AWS/GCP/Azure secrets managers | Cloud-native apps |
| HashiCorp Vault | Multi-cloud, dynamic secrets, mature |
| Sealed Secrets / SOPS | GitOps workflows where secrets must live in repo (encrypted) |
| Doppler / 1Password Secrets Automation | Small teams, dev experience focus |

## Cloud Platform Selection

| Workload shape | Best fit | Why |
|---|---|---|
| Stateless web/API, low ops appetite | Vercel, Netlify, Fly.io | Edge, zero-config, fast iteration |
| Containerized services, mid scale | AWS ECS, GCP Cloud Run | Managed runtime, no K8s overhead |
| Complex microservices, ops capacity | EKS / GKE / AKS | Full K8s control |
| Heavy data, ML training | AWS / GCP with managed services | Mature data + ML stacks |
| Compliance-heavy (HIPAA, FedRAMP) | AWS GovCloud, Azure Government | Already accredited |

Pick by team capacity, not hype. Kubernetes is a tax most teams should not pay until product fit is proven.

## Common Failure Modes

- **Image is 2 GB** — missing `.dockerignore`, missing multi-stage, packing dev deps
- **Container OOM-kills under load** — no resource limits, or limits set too low for actual workload
- **Liveness probe causes restart loops** — probe hits a slow endpoint or starts before warmup
- **Secrets leaked in CI logs** — masked as `***` only if registered with the runner; raw `echo` of env vars exposes them
- **Terraform state lock stuck** — operator killed mid-apply; need to manually break the lock after confirming no apply is running

## Integration

- `skill-deployment` — release strategy/pipeline that ships changes to this infrastructure
- `skill-observability` — instruments running on top of this infra (metrics, traces, logs)
- `skill-backend` / `skill-frontend` — application code that runs in the containers
- `shared/skill-security` — securing the cluster, secrets, IAM, supply chain
- `shared/skill-debugging` — investigating production incidents on this infra

## Resources

- [Docker BuildKit reference](https://docs.docker.com/build/buildkit/)
- [Kubernetes Production Best Practices](https://learnk8s.io/production-best-practices)
- [Terraform best practices](https://www.terraform-best-practices.com/)
- [The Twelve-Factor App](https://12factor.net/)
