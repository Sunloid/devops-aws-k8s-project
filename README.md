# devops-aws-k8s-project

Code (app/) 
   → Docker image (Dockerfile) 
      → AWS infra exists (Terraform: VPC + EKS + ECR) 
         → Image pushed to ECR 
            → Kubernetes manifests deploy it onto EKS (Deployment/Service/Ingress) 
               → App is live and reachable 
                  → CI/CD automates repeating this on every code change 
                     → Monitoring watches it in production