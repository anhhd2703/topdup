module "prod_vpc" {
  source  = "../../../modules//terraform-aws-vpc"

  name = "topdup-prod"
  cidr = "100.65.0.0/16"

  azs             = ["ap-southeast-1a", "ap-southeast-1b", "ap-southeast-1c"]
  private_subnets = ["100.65.0.0/19", "100.65.32.0/19", "100.65.64.0/19", "100.65.96.0/19"]
  public_subnets  = ["100.65.128.0/19", "100.65.160.0/19", "100.65.192.0/19", "100.65.224.0/19"]

  enable_nat_gateway     = true
  single_nat_gateway     = true
  one_nat_gateway_per_az = false
  enable_vpn_gateway     = false
  enable_dns_hostnames   = true

  tags = {
    Terraform = "true"
    Environment = "topdup-prod"
  }
}
