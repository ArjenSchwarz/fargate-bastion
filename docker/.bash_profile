# Enable bash completion
source /usr/share/bash-completion/bash_completion

# Enable kubectl autocompletion
source <(kubectl completion bash)

# Enable eksctl autocompletion
source <(eksctl completion bash)

# Enable AWS CLI autocompletion
complete -C '/usr/local/bin/aws_completer' aws

# region=$(curl --silent 169.254.170.2/v2/metadata | jq -r .TaskARN | cut -d: -f4)
# export AWS_DEFAULT_REGION=${region}
# export AWS_REGION=${region}

# echo "Your region has been set to ${region}"

echo "Please load your AWS credentials (e.g. using 'export AWS_ACCESS_KEY_ID=youraccess; export AWS_SECRET_ACCESS_KEY=yoursecret')"
echo "Then run 'aws eks update-kubeconfig --name cluster_name' to configure your kube config"