locals {
  demoexpgen_fname    = "${var.unique_identifier}_lambda_demoexpgen"
  demoexpgen_loggroup = "/aws/lambda/${local.demoexpgen_fname}"
}

provider "aws" {
  region = var.aws_region
}

provider "archive" {}
