module "staging_database" {
  source = "../../../modules/terraform-aws-ec2-instance"

  name                   = "topdup-staging-database"
  instance_count         = 1
  ami                    = "ami-06fb5332e8e3e577a"
  instance_type          = "t3.micro"
  key_name               = "topdup-staging"
  root_block_device = [
    {
      volume_size           = 20
      delete_on_termination = true
    }
  ]

  ebs_block_device = [
    {
      device_name = "/dev/sdf"
      volume_type = "gp2"
      volume_size = 30
    }
  ]

  disable_api_termination     = true
  vpc_security_group_ids      = tolist([module.staging_database_secgroup.this_security_group_id])
  subnet_ids                  = data.terraform_remote_state.staging_vpc.outputs.staging_vpc_public_subnets

  tags = {
    Terraform   = "true"
    Environment = "topdup-staging"
    Function    = "database"
    Description = "PostgreSQL"
  }
}

module "staging_database_secgroup" {
  source  = "../../../modules/terraform-aws-security-group"

  name        = "database_secgroup"
  description = "Security group for Database Ec2 instance"
  vpc_id      = data.terraform_remote_state.staging_vpc.outputs.staging_vpc_id

  ingress_cidr_blocks = ["0.0.0.0/0"]
  ingress_rules       = ["ssh-tcp", "all-icmp", "postgresql-tcp"]
  egress_rules        = ["all-all"]
}
