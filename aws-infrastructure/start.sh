#!/bin/bash
set -x

# Generate RSA key for ssh access if not exists
if [ ! -f "aws_ssh_key" ]
then
    ssh-keygen -t rsa -b 4096 -f aws_ssh_key -N ""
fi

# Start AWS infrotructure
terraform init
terraform apply -input=false -auto-approve

# Export terraform output variables
export PRIVATE_CLIENT_IP_ADDR=$(terraform output private_client_ip_addr)
export PRIVATE_SERVER_IP_ADDR=$(terraform output private_server_ip_addr)
export PUBLIC_CLIENT_IP_ADDR=$(terraform output public_client_ip_addr)
export PUBLIC_SERVER_IP_ADDR=$(terraform output public_server_ip_addr)