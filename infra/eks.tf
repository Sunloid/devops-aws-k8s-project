module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = var.cluster_name
  cluster_version = "1.31"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets   # worker nodes go in private subnets

  # Makes the cluster API reachable from your laptop for kubectl/testing.
  # In a stricter real-world setup this would be locked down further.
  cluster_endpoint_public_access = true

  eks_managed_node_groups = {
    default = {
      min_size     = 1
      max_size     = 2
      desired_size = 1

      instance_types = ["t3.medium"]   # cheapest practical instance type for EKS nodes
      capacity_type  = "ON_DEMAND"
    }
  }

  # Gives your current AWS CLI user admin access to the cluster via kubectl
  enable_cluster_creator_admin_permissions = true
}
