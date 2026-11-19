output "resource_group_name" {
  value = azurerm_resource_group.this.name
}

output "aks_name" {
  value = module.aks.name
}

output "acr_login_server" {
  value = module.acr.login_server
}

output "postgres_fqdn" {
  value = module.postgres.fqdn
}

output "postgres_database" {
  value = module.postgres.database_name
}
