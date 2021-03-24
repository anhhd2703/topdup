data "terraform_remote_state" "staging_vpc" {
  backend = "s3"
  config  = {
    bucket  = "infra-remotestates"
    key     = "staging/vpc"
    region  = "ap-southeast-1"
  }
}
