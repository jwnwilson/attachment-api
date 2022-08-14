/* general */
variable "environment" {
  default = "develop"
}

variable "aws_region" {
  default = "eu-west-1"
}

variable "region" {
  default = "eu-west-1"
}

variable "aws_access_key" {
}

variable "aws_secret_key" {
}

variable "project" {
  default = "attachment-service"
}

variable "ecr_api_url" {}

variable "docker_tag" {
  default = "latest"
}

variable "domain" {
  default = "jwnwilson.co.uk"
}

variable "api_subdomain" {
  default = "attachment"
}

variable "ecr_url" {
  description = "Name of container image repository"
  default     = "attachment_service_api"
}