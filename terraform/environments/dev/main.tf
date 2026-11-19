resource "azurerm_resource_group" "this" {
  name     = "${var.name_prefix}-rg"
  location = var.location
}

module "network" {
  source              = "../../modules/network"
  name_prefix         = var.name_prefix
  location            = var.location
  resource_group_name = azurerm_resource_group.this.name
}

module "acr" {
  source              = "../../modules/acr"
  name                = var.acr_name
  location            = var.location
  resource_group_name = azurerm_resource_group.this.name
}

module "aks" {
  source              = "../../modules/aks"
  name_prefix         = var.name_prefix
  location            = var.location
  resource_group_name = azurerm_resource_group.this.name
  subnet_id           = module.network.aks_subnet_id
  acr_id              = module.acr.id
  node_vm_size        = var.node_vm_size
}

module "postgres" {
  source              = "../../modules/postgres"
  name                = var.postgres_server_name
  location            = var.location
  resource_group_name = azurerm_resource_group.this.name
  delegated_subnet_id = module.network.postgres_subnet_id
  private_dns_zone_id = module.network.postgres_private_dns_zone_id
  admin_username      = var.postgres_admin_username
  admin_password      = var.postgres_admin_password

  # The DNS zone's VNet link must exist before the server is created.
  depends_on = [module.network]
}
