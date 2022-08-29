terraform {
  backend "s3" {
    region = "eu-west-1"
    bucket = "jwnwilson-attachment-api-tf"
    key = "terraform.tfstate"
  }
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region  = var.aws_region
}

module "attachment_api" {
  source = "github.com/jwnwilson/terraform-aws-modules/modules/lambda-api"

  environment       = var.environment
  project           = "attachment"
  ecr_url           = var.ecr_url
  docker_tag        = var.docker_tag
  region            = var.aws_region
  aws_access_key    = var.aws_access_key
  aws_secret_key    = var.aws_secret_key
  lambda_command    = ["app.adapter.into.fastapi.lambda.handler"]
}

module "api_gateway" {
  source = "github.com/jwnwilson/terraform-aws-modules/modules/apigateway-authorizer"

  environment       = var.environment
  lambda_invoke_arn = module.attachment_api.lambda_function_invoke_arn
  lambda_name       = module.attachment_api.lambda_function_name
  domain            = "jwnwilson.co.uk"
  api_subdomain     = "attachment-${var.environment}"
  project           = "attachment"
  authorizer_name   = "authorizer_api_gw_${var.environment}"
}

resource "aws_iam_user" "upload_user" {
  name    = "attachment_upload_user_${var.environment}"
  path    = "/"
}

resource "aws_iam_access_key" "upload_user" {
  user    = aws_iam_user.upload_user.name
}

resource "aws_iam_user_policy" "upload_user_s3" {
  name = "email_upload_user_s3_${var.environment}"
  user = aws_iam_user.upload_user.name

  policy = <<EOF
{
  "Version": "2008-10-17",
  "Statement": [{
    "Sid": "AllowAccessInAWS",
    "Effect": "Allow",
    "Action": ["s3:*"],
    "Resource": [
      "arn:aws:s3:::jwnwilson-attachments-${var.environment}/*",
    ]
  }]
}
EOF
}

resource "aws_ssm_parameter" "upload_access_id" {
  name  = "/attachment-api/upload_access_id_${var.environment}"
  type  = "String"
  value = aws_iam_access_key.upload_user.id
}

resource "aws_ssm_parameter" "upload_secret_key" {
  name  = "/attachment-api/upload_secret_key_${var.environment}"
  type  = "String"
  value = aws_iam_access_key.upload_user.secret
}



resource "aws_iam_policy" "s3-lambda-policy" {
  name        = "${var.project}-s3-lambda-policy-${var.environment}"
  description = "lambda s3 policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
        "Sid": "AllS3Actions",
        "Effect": "Allow",
        "Action": "s3:*",
        "Resource": [
          "arn:aws:s3:::jwnwilson-attachments-${var.environment}/*",
          "*"
        ]
    },
    {
        "Effect": "Allow",
        "Action": [
            "ssm:DescribeParameters",
            "ssm:GetParameters",
            "ssm:GetParameter"
        ],
        "Resource": [
          "arn:aws:ssm:eu-west-1:675468650888:parameter/attachment-api/upload_access_id_${var.environment}",
          "arn:aws:ssm:eu-west-1:675468650888:parameter/attachment-api/upload_secret_key_${var.environment}"
        ]
    },
    {
        "Effect": "Allow",
        "Action": [
            "ses:*"
        ],
        "Resource": [
          "arn:aws:ses:eu-west-1:675468650888:*"
        ]
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "s3" {
  role       = module.attachment_api.lambda_role_name
  policy_arn = aws_iam_policy.s3-lambda-policy.arn
}

resource "aws_s3_bucket" "attachment_storage" {
  bucket = "jwnwilson-attachments-${var.environment}"
  acl    = "private"

  policy = <<EOF
  {
    "Version": "2008-10-17",
    "Statement": [{
      "Sid": "AllowAccessInAWS",
      "Effect": "Allow",
      "Principal": { "AWS": "*" },
      "Action": ["s3:*"],
      "Resource": ["arn:aws:s3:::jwnwilson-attachments-${var.environment}/*" ]
    }]
  }
  EOF

  tags = {
    Name        = "Attachment bucket${var.environment} "
    Environment = var.environment
  }
}
