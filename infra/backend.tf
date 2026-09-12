terraform {
  backend "s3" {
    bucket         = "sunloid-devops-practice-tfstate"
    key            = "eks/terraform.tfstate"   # path inside the bucket where state is stored
    region         = "ap-south-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
