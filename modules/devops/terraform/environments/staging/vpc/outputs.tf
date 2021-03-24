output "staging_vpc_id" {
  value = module.staging_vpc.vpc_id
}

output "staging_vpc_private_subnets" {
  value = module.staging_vpc.private_subnets
}

output "staging_vpc_public_subnets" {
  value = module.staging_vpc.public_subnets
}

