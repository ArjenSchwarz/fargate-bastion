# Fargate Bastion

Serverless bastions on demand.

Fargate bastions let you spin up a bastion host when you need, and only while you need it. Access to the bastions is limited to your IP address, and each is tailored to you. A high-level overview can be found in [my blogpost].(https://ig.nore.me/2018/07/serverless-bastions-on-demand/)

## Components

### bastion-lambda.yml

The main component is the `bastion-lambda.yml` SAM template. This spins up the API Gateway as well as the Lambda functions used to create or destroy the Fargate instances.

You can run this up with the below command (please replace the parameters and placeholders with your own values)

```bash
aws cloudformation package --template-file bastion-lambda.yml --s3-bucket "$YOURS3BUCKET" --output-template-file packaged-bastion.yml
aws cloudformation deploy --template-file packaged-bastion.yml --stack-name bastion-functions --capabilities CAPABILITY_IAM --parameter-overrides BastionVpc=vpc-12345678 BastionSubnets=subnet-12345678 BastionCluster=default CleanupSchedule="cron(0 14 * * ? *)"
```

which gives you the functions needed.

### container-pipeline.yml

This builds a codebuild job that creates the Docker images and uploads them to ECR. It pulls the public keys from the SSM Parameter Store.

### codebuild-vpc.yml

This builds a VPC that can be used by CodeBuild as CodeBuild can only run in a subnet that has access to the outside world through a NAT Gateway.

### ecs-cluster.yml

This builds an empty ECS cluster if you don't have one yet.