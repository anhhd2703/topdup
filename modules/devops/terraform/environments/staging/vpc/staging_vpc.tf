module "staging_vpc" {
  source  = "../../../modules//terraform-aws-vpc"

  name = "topdup-staging"
  cidr = "100.64.0.0/16"

  azs             = ["ap-southeast-1a", "ap-southeast-1b", "ap-southeast-1c"]
  private_subnets = ["100.64.0.0/19", "100.64.32.0/19", "100.64.64.0/19", "100.64.96.0/19"]
  public_subnets  = ["100.64.128.0/19", "100.64.160.0/19", "100.64.192.0/19", "100.64.224.0/19"]

  enable_nat_gateway     = true
  single_nat_gateway     = true
  one_nat_gateway_per_az = false
  enable_vpn_gateway     = false
  enable_dns_hostnames   = true

  tags = {
    Terraform = "true"
    Environment = "topdup-staging"
  }
}
