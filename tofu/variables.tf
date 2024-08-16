variable "env" {
    description = "The environment for the deployment (e.g., dev, staging, prod)"
    type        = string
    default     = "dev"
}

variable "project_name" {
    description = "The name of the project"
    type        = string
    default     = "quack"
}