terraform {
  required_version = ">= 1.16.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }

    snowflake = {
      source  = "snowflakedb/snowflake"
      version = "~> 2.21"
    }
  }

  backend "s3" {
    bucket       = "filingpulse-tfstate-7806b2bd5f8c57885d98e355b5"
    key          = "filingpulse/dev/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
}

provider "aws" {
  region = var.aws_region
}

provider "snowflake" {
  organization_name = "KDPJJHH"
  account_name      = "ftb83569"
  user              = "MAIRAJ10"
  role              = "ACCOUNTADMIN"

  authenticator = "SNOWFLAKE_JWT"
  private_key   = file(pathexpand("~/.snowflake/filingpulse/rsa_key.p8"))
  private_key_passphrase = var.snowflake_private_key_passphrase
}

