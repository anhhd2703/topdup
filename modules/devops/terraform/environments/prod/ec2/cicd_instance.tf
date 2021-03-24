module "cicd" {
  source = "../../../modules/terraform-aws-ec2-instance"

  name                   = "topdup-cicd"
  instance_count         = 1
  ami                    = "ami-06fb5332e8e3e577a"
  instance_type          = "t3a.medium"
  key_name               = "topdup-prod"
  user_data              = base64encode(local.user_data)
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
      volume_size = 100
    }
  ]

  disable_api_termination     = true
  vpc_security_group_ids      = tolist([module.prod_cicd_secgroup.this_security_group_id])
  subnet_ids                  = data.terraform_remote_state.prod_vpc.outputs.prod_vpc_public_subnets

  tags = {
    Name        = "topdup-cicd"
    Terraform   = "true"
    Environment = "topdup-prod"
    Function    = "cicd"
  }
}

resource "aws_eip" "lb" {
  instance = module.cicd.id[0]
  vpc      = true
}

module "prod_cicd_secgroup" {
  source  = "../../../modules/terraform-aws-security-group"

  name        = "cicd_secgroup"
  description = "Security group for Database Ec2 CiCd"
  vpc_id      = data.terraform_remote_state.prod_vpc.outputs.prod_vpc_id

  ingress_cidr_blocks = ["0.0.0.0/0"]
  ingress_rules       = ["ssh-tcp", "all-icmp", "https-443-tcp"]
  ingress_with_cidr_blocks = [
    {
      from_port   = 51820
      to_port     = 51820
      protocol    = "tcp"
      description = "Allow Wireguard VPN"
      cidr_blocks = "0.0.0.0/0"
    },
    {
      from_port   = 51820
      to_port     = 51820
      protocol    = "udp"
      description = "Allow Wireguard VPN"
      cidr_blocks = "0.0.0.0/0"
    }
  ]

  egress_rules        = ["all-all"]
}
