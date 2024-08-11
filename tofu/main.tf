terraform {
    backend "s3" {
        bucket = "tf-state-dev-9750"
        key    = "quack/terraform.tfstate"
        region = "us-east-1"
      
    }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "quack_bucket" {
  bucket = "quack-bucket"
}

resource "aws_ecr_repository" "quack_ecr" {
  name = "quack-ingest"
}