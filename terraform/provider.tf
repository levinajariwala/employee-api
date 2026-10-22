terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "amzn-dms-demo-bucket"
    key    = "terraform/terraform.tfstate"
    region = "eu-west-2"
  }
}

provider "aws" {
  region = var.region
}