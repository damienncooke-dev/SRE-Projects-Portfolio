# Terraform AWS Infrastructure Automation — SRE Portfolio Project

> **Purpose:** Demonstrates Infrastructure-as-Code proficiency using Terraform on AWS, covering beginner-to-intermediate concepts aligned with SRE environment automation roles. This project provisions multi-environment AWS infrastructure with a focus on modularity, state management, security, and operational best practices.

---

## Project Overview

This project provisions a realistic, multi-environment AWS infrastructure (dev / staging / prod) using Terraform. It demonstrates core SRE competencies including IaC lifecycle management, remote state, modular design, IAM least-privilege, and observability — mapped directly to the skills expected in environment automation roles.

**Tech Stack:** Terraform · AWS (IAM, S3, DynamoDB, VPC, EC2, CloudWatch) · GitHub Actions CI/CD

---

## Repository Structure

```
terraform-aws-sre-demo/
├── README.md
├── modules/
│   ├── iam/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── s3/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── dynamodb/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── monitoring/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   └── prod/
│       ├── main.tf
│       ├── variables.tf
│       ├── terraform.tfvars
│       └── backend.tf
├── .github/
│   └── workflows/
│       └── terraform-ci.yml
├── .gitignore
└── docs/
    ├── architecture.md
    └── runbook.md
```

---

## Phase 1 — Terraform Foundations & Remote State Bootstrap

**Concepts demonstrated:** provider configuration, backend setup, S3 state storage, DynamoDB state locking, `.gitignore` for sensitive files.

### 1.1 Provider Configuration

- Configure the `aws` provider with region variable
- Pin provider version with `required_providers` block
- Use `terraform.required_version` constraint

### 1.2 S3 Backend for Remote State

Provision an S3 bucket to store Terraform state files remotely:

- Enable versioning on the state bucket (supports state rollback)
- Enable server-side encryption (SSE-S3 or SSE-KMS)
- Block all public access
- Enable access logging to a separate S3 bucket

```hcl
# bootstrap/main.tf — run once to create the backend infrastructure
resource "aws_s3_bucket" "tf_state" {
  bucket = "your-org-terraform-state"
  # ... versioning, encryption, public access block
}
```

### 1.3 DynamoDB State Locking Table

Provision a DynamoDB table to prevent concurrent state modifications:

- `LockID` as the partition key (String)
- PAY_PER_REQUEST billing mode
- Point-in-time recovery enabled

```hcl
resource "aws_dynamodb_table" "tf_lock" {
  name         = "terraform-state-lock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
```

### 1.4 Backend Configuration Per Environment

Configure each environment to use the shared S3 backend with a unique state key:

```hcl
# environments/dev/backend.tf
terraform {
  backend "s3" {
    bucket         = "your-org-terraform-state"
    key            = "environments/dev/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}
```

**SRE relevance:** Remote state with locking mirrors how teams safely manage IaC across many tenant environments without state corruption.

---

## Phase 2 — IAM: Identity and Least-Privilege Access

**Concepts demonstrated:** IAM roles, policies, instance profiles, policy attachment, data sources, least-privilege design.

### 2.1 IAM Module Structure (`modules/iam/`)

- Accept `environment` and `app_name` as input variables
- Output role ARN and instance profile name for consumption by other modules

### 2.2 IAM Role for EC2 (Instance Profile)

- Create an IAM role with an EC2 trust policy
- Attach a custom policy granting only the permissions needed (e.g., read from a specific S3 bucket, write to a specific DynamoDB table)
- Create an instance profile to attach the role to EC2 instances

```hcl
resource "aws_iam_role" "app_role" {
  name               = "${var.app_name}-${var.environment}-role"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role.json
}
```

### 2.3 Custom IAM Policy (Least Privilege)

- Use `aws_iam_policy_document` data source to build policies in HCL (not JSON strings)
- Scope permissions to specific resource ARNs using `module.s3.bucket_arn` and `module.dynamodb.table_arn` output references

### 2.4 Demonstrate Cross-Module Reference

Show how the IAM module consumes outputs from the S3 and DynamoDB modules to scope permissions to exact resource ARNs — illustrating module composition.

### 2.5 (Stretch) IAM for CI/CD Pipeline

- Create a dedicated IAM user or role for GitHub Actions with scoped permissions
- Use OIDC federation to avoid long-lived access keys (GitHub Actions → AWS trust relationship)

**SRE relevance:** Demonstrates understanding of isolation and least-privilege — critical when managing many tenant environments where blast radius must be minimized.

---

## Phase 3 — S3: Storage, Lifecycle, and Environment Isolation

**Concepts demonstrated:** resource configuration, conditional expressions, `for_each`, lifecycle rules, tagging strategy.

### 3.1 S3 Module (`modules/s3/`)

Inputs: `bucket_name_prefix`, `environment`, `enable_versioning`, `lifecycle_enabled`
Outputs: `bucket_id`, `bucket_arn`, `bucket_domain_name`

### 3.2 Environment-Specific Buckets

Provision separate S3 buckets per environment using a naming convention:

```
{prefix}-{environment}-{aws_account_id}
```

- Enforce bucket name uniqueness with account ID interpolation
- Tag all resources with `Environment`, `ManagedBy = "terraform"`, `Project`

### 3.3 Versioning and Lifecycle Rules

- Enable versioning conditionally based on `var.enable_versioning`
- Configure lifecycle rule to transition objects to `STANDARD_IA` after 30 days and expire noncurrent versions after 90 days (dev) vs. 365 days (prod)

```hcl
resource "aws_s3_bucket_lifecycle_configuration" "this" {
  count  = var.lifecycle_enabled ? 1 : 0
  bucket = aws_s3_bucket.this.id
  # ... rules
}
```

### 3.4 Public Access Block and Bucket Policy

- Block all public access on every bucket
- Attach a bucket policy enforcing HTTPS-only access (`aws:SecureTransport`)

### 3.5 Access Logging

Route S3 access logs from application buckets to a dedicated logging bucket — demonstrates defense-in-depth and audit trail thinking.

**SRE relevance:** Mirrors artifact/log storage patterns used in environment lifecycle management, including backup and retention policies.

---

## Phase 4 — DynamoDB: Application Data and State Store

**Concepts demonstrated:** NoSQL provisioning, capacity modes, TTL, stream configuration, tagging.

### 4.1 DynamoDB Module (`modules/dynamodb/`)

Inputs: `table_name`, `environment`, `billing_mode`, `enable_ttl`, `enable_streams`
Outputs: `table_arn`, `table_name`, `stream_arn`

### 4.2 Core Table Configuration

- Configure hash key and optional range key via variables
- Support both `PAY_PER_REQUEST` (dev/staging) and `PROVISIONED` (prod) billing modes using a conditional
- Enable point-in-time recovery (PITR) in prod

```hcl
resource "aws_dynamodb_table" "this" {
  name         = "${var.table_name}-${var.environment}"
  billing_mode = var.billing_mode
  hash_key     = var.hash_key

  point_in_time_recovery {
    enabled = var.environment == "prod" ? true : false
  }
}
```

### 4.3 TTL Configuration

Enable TTL on a configurable attribute for session or ephemeral data — demonstrate operational understanding of data expiration.

### 4.4 DynamoDB Streams (Stretch)

Enable DynamoDB Streams and output the stream ARN for downstream consumption (e.g., Lambda trigger) — demonstrates design awareness for event-driven patterns.

### 4.5 Environment-Differentiated Configuration

Show `terraform.tfvars` differences across environments:

| Setting | dev | staging | prod |
|---|---|---|---|
| `billing_mode` | PAY_PER_REQUEST | PAY_PER_REQUEST | PROVISIONED |
| `enable_pitr` | false | false | true |
| `enable_streams` | false | true | true |

**SRE relevance:** Demonstrates ability to differentiate infrastructure configuration per environment — a core requirement when operating many tenant environments.

---

## Phase 5 — Networking: VPC and Security Groups

**Concepts demonstrated:** VPC, subnets, routing, security groups, `cidrsubnet()` function, data sources.

### 5.1 VPC Module (`modules/vpc/`)

Inputs: `vpc_cidr`, `environment`, `az_count`, `enable_nat_gateway`
Outputs: `vpc_id`, `public_subnet_ids`, `private_subnet_ids`

### 5.2 VPC and Subnet Provisioning

- Create a VPC with a CIDR block passed as a variable
- Use `data "aws_availability_zones"` to dynamically discover AZs
- Use `count` and `cidrsubnet()` to generate public and private subnets across AZs

```hcl
resource "aws_subnet" "private" {
  count             = var.az_count
  vpc_id            = aws_vpc.this.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]
}
```

### 5.3 Internet Gateway and NAT Gateway

- Attach an IGW for public subnets
- Conditionally provision a NAT Gateway for private subnet egress (`var.enable_nat_gateway`)
- Skip NAT Gateway in dev to reduce cost; enable in prod

### 5.4 Security Groups

- Create a baseline security group: no ingress, allow all egress
- Create an app-tier security group: allow inbound on app port from within VPC CIDR only
- Demonstrate SG rule references (SG-to-SG vs. CIDR-based rules)

**SRE relevance:** Network isolation is foundational to the single-tenant GitLab Dedicated model; demonstrates understanding of environment boundary enforcement.

---

## Phase 6 — Multi-Environment Orchestration

**Concepts demonstrated:** workspace-vs-directory pattern, `terraform.tfvars`, variable validation, `locals`, module composition.

### 6.1 Directory-Based Environment Isolation

Use separate directories under `environments/` (not workspaces) for strict environment isolation — each has its own state file and can be applied independently.

Explain *why*: workspace-based approaches share a backend config and are prone to accidental cross-environment applies at scale.

### 6.2 Root Module Composition

Each environment's `main.tf` calls all modules and wires outputs between them:

```hcl
# environments/prod/main.tf
module "vpc" {
  source           = "../../modules/vpc"
  environment      = var.environment
  vpc_cidr         = var.vpc_cidr
  az_count         = 3
  enable_nat_gateway = true
}

module "s3" {
  source              = "../../modules/s3"
  environment         = var.environment
  bucket_name_prefix  = var.project_name
  enable_versioning   = true
  lifecycle_enabled   = true
}

module "dynamodb" {
  source        = "../../modules/dynamodb"
  environment   = var.environment
  table_name    = var.project_name
  billing_mode  = "PROVISIONED"
  enable_pitr   = true
}

module "iam" {
  source          = "../../modules/iam"
  environment     = var.environment
  app_name        = var.project_name
  s3_bucket_arn   = module.s3.bucket_arn
  dynamodb_table_arn = module.dynamodb.table_arn
}
```

### 6.3 Variable Validation

Add `validation` blocks to catch misconfiguration early:

```hcl
variable "environment" {
  type = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment must be one of: dev, staging, prod."
  }
}
```

### 6.4 Locals for Computed Values

Use `locals` for derived values and common tags to avoid repetition:

```hcl
locals {
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
    Owner       = "sre-team"
  }
  is_prod = var.environment == "prod"
}
```

---

## Phase 7 — Observability and Monitoring

**Concepts demonstrated:** CloudWatch alarms, log groups, metric filters, SNS alerting, data-driven resource creation.

### 7.1 Monitoring Module (`modules/monitoring/`)

Inputs: `environment`, `s3_bucket_id`, `dynamodb_table_name`, `alarm_email`
Outputs: `sns_topic_arn`

### 7.2 CloudWatch Log Group

- Provision a CloudWatch Log Group with configurable retention (shorter in dev, longer in prod)
- Tag with `Environment` and `ManagedBy`

### 7.3 CloudWatch Alarms

Create alarms for:

| Alarm | Metric | Threshold |
|---|---|---|
| DynamoDB throttled requests | `ThrottledRequests` | > 0 for 5 min |
| S3 4xx errors | `4xxErrors` | > 10 for 5 min |
| DynamoDB consumed write capacity | `ConsumedWriteCapacityUnits` | > 80% of provisioned |

### 7.4 SNS Topic for Alert Routing

- Create an SNS topic and email subscription for alarm notifications
- Demonstrate use of `aws_sns_topic_subscription` with a variable email endpoint

### 7.5 `for_each` for Multiple Alarms

Use a `for_each` over a `map` of alarm definitions to avoid duplicating alarm resource blocks — demonstrates DRY Terraform patterns:

```hcl
locals {
  dynamodb_alarms = {
    throttled_reads  = { metric = "ReadThrottleEvents",  threshold = 1 }
    throttled_writes = { metric = "WriteThrottleEvents", threshold = 1 }
  }
}

resource "aws_cloudwatch_metric_alarm" "dynamodb" {
  for_each = local.dynamodb_alarms
  # ...
}
```

**SRE relevance:** Directly maps to the JD requirement to "build and refine the observability stack" and "monitor the right signals."

---

## Phase 8 — CI/CD Pipeline (GitHub Actions)

**Concepts demonstrated:** pipeline-driven IaC, automated `plan` on PR, gated `apply` on merge, OIDC auth, environment promotion.

### 8.1 Workflow File (`.github/workflows/terraform-ci.yml`)

Define a workflow with two jobs:

**Job 1 — `terraform-plan` (on PR):**
1. Checkout code
2. Configure AWS credentials via OIDC (no long-lived keys)
3. `terraform init`
4. `terraform validate`
5. `terraform fmt --check`
6. `terraform plan -out=tfplan`
7. Post plan output as PR comment

**Job 2 — `terraform-apply` (on merge to `main`):**
1. Checkout code
2. Configure AWS credentials via OIDC
3. `terraform init`
4. `terraform apply -auto-approve tfplan`

### 8.2 Environment Matrix (Stretch)

Use a matrix strategy to run plan/apply across `dev`, `staging`, `prod` in sequence, with staging requiring dev success and prod requiring staging success.

### 8.3 OIDC Authentication (No Static Keys)

Configure the GitHub Actions OIDC provider in AWS:
- `aws_iam_openid_connect_provider` resource
- IAM role with a trust policy that allows federation from the specific GitHub repo

**SRE relevance:** Demonstrates safe, automated IaC delivery — a core mechanism for managing upgrades and configuration changes at scale without manual intervention.

---

## Phase 9 — Terraform Operations and State Management

**Concepts demonstrated:** `terraform import`, `terraform state mv`, `terraform taint`, `terraform output`, drift detection.

### 9.1 Document Common Operational Commands

Include a runbook (`docs/runbook.md`) covering:

```bash
# Initialize with backend
terraform init

# Preview changes for a specific environment
cd environments/dev && terraform plan

# Apply changes
terraform apply

# Inspect state
terraform state list
terraform state show module.s3.aws_s3_bucket.this

# Import an existing resource into state
terraform import module.s3.aws_s3_bucket.this my-existing-bucket

# Move a resource in state after refactoring
terraform state mv aws_s3_bucket.old module.s3.aws_s3_bucket.this

# Force replacement of a resource
terraform taint module.dynamodb.aws_dynamodb_table.this

# View outputs
terraform output -json
```

### 9.2 Drift Detection

Document the pattern for detecting configuration drift:
- Run `terraform plan` in CI on a schedule (e.g., nightly cron)
- Alarm if plan output is non-empty (resources have drifted from declared state)

### 9.3 State Backup and Recovery

- Document how S3 versioning on the state bucket enables rollback
- Show how to restore a previous state version via AWS Console or CLI

**SRE relevance:** State management proficiency is explicitly called out in the JD ("managing state safely for multiple environments") and is critical for multi-tenant operations.

---

## Key Concepts Reference

| Concept | Where Demonstrated |
|---|---|
| Remote state (S3 backend) | Phase 1 |
| State locking (DynamoDB) | Phase 1 |
| Modular design | Phases 2–7 (all modules) |
| Variable validation | Phase 6.3 |
| `count` and `for_each` | Phases 3, 5, 7 |
| `locals` | Phase 6.4 |
| Cross-module references (outputs) | Phase 6.2 |
| Conditional expressions | Phases 3, 4, 5 |
| `cidrsubnet()` function | Phase 5.2 |
| Data sources | Phase 5.2, 2.3 |
| IAM least-privilege | Phase 2 |
| Lifecycle rules | Phase 3.3 |
| Multi-environment isolation | Phase 6 |
| Observability with CloudWatch | Phase 7 |
| CI/CD pipeline (GitHub Actions) | Phase 8 |
| OIDC auth (no static keys) | Phase 8.3 |
| Drift detection | Phase 9.2 |
| State operations (`import`, `mv`, `taint`) | Phase 9.1 |
| Tagging strategy | Phases 3, 4, 6.4 |

---

## Architecture Diagram

> Add a diagram to `docs/architecture.md` showing:
> - Three environment lanes (dev / staging / prod)
> - S3 remote state bucket and DynamoDB lock table (shared bootstrap layer)
> - Per-environment: VPC → EC2 (with IAM instance profile) → S3 bucket → DynamoDB table → CloudWatch alarms → SNS
> - GitHub Actions pipeline triggering across environments

---

## How This Maps to the GitLab SRE JD

| JD Requirement | Demonstrated Here |
|---|---|
| Terraform modules, variables, state management for multiple environments | All phases |
| Infrastructure lifecycle: provisioning, upgrades, configuration changes | Phases 1–6, 8–9 |
| Reducing manual toil through automation | Phase 8 (CI/CD), Phase 9.2 (drift detection) |
| Observability stack | Phase 7 |
| Runbooks and repeatable operational processes | Phase 9, `docs/runbook.md` |
| Git-based IaC workflows | Phase 8, PR-driven plan/apply |
| IAM least-privilege and security | Phase 2 |
| Environment isolation | Phase 6, VPC module |

---

## Getting Started

### Prerequisites

- Terraform >= 1.6
- AWS CLI configured with appropriate credentials
- GitHub repository with Actions enabled
- (Optional) AWS account with sufficient IAM permissions to create all resources above

### Bootstrap (One-time)

```bash
cd bootstrap/
terraform init
terraform apply
```

### Provision an Environment

```bash
cd environments/dev/
terraform init
terraform plan
terraform apply
```

### Tear Down

```bash
terraform destroy
```

---

## License

MIT
