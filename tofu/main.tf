terraform {
    backend "s3" {
        bucket = "tf-state-dev-9750"
        key    = "${var.project_name}/terraform.tfstate"
        region = "us-east-1"
      
    }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "lance_bucket" {
  bucket = "${var.project_name}-lance-bucket-${var.env}"
}

resource "aws_ecr_repository" "lambda_ecr" {
  name = "${var.project_name}-ingest-${var.env}-ecr"
}