variable "name_prefix" {
  description = "Short prefix for Azure resource names."
  type        = string
  default     = "cloudops-dev"
}

variable "location" {
  description = "Azure region."
  type        = string
  default     = "eastus"
}

variable "acr_name" {
  description = "Globally unique ACR name: 5-50 alphanumeric characters."
  type        = string
}

variable "postgres_server_name" {
  description = "Globally unique PostgreSQL Flexible Server name."
  type        = string
}

variable "postgres_admin_username" {
  type    = string
  default = "cloudopsadmin"
}

variable "postgres_admin_password" {
  description = "PostgreSQL administrator password; supply through TF_VAR_postgres_admin_password."
  type        = string
  sensitive   = true
}

variable "node_vm_size" {
  type    = string
  default = "Standard_D2s_v5"
}
