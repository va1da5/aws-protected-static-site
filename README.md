# Protected Static Site in AWS S3

The repository contains a Terraform configuration for deploying a static site to [AWS S3 bucket](https://aws.amazon.com/s3/) and exposing it using [AWS CloudFront](https://aws.amazon.com/cloudfront/). The site is protected by a basic authentication using [Lambda@Edge](https://aws.amazon.com/lambda/edge/).

The static site is located in [public](public/) directory. Currently it contains an awesome CSS based visualization borrowed from [CodePen: CSS Mars Landing](https://codepen.io/mgitch/pen/pECcD). The authentication is achieved using Lambda@Edge Python function located in [aws_lambda](aws_lambda/) directory. It is a good security practice to store secrets in AWS Secrets Managers, however, this example utilizes a flat-file for credentials storage which is later bundled together with the Lambda function.


The [Lambda@Edge](https://aws.amazon.com/lambda/edge/) does not allow usage of environment variables, however, this functionality could be still achieved by using [python-dotenv](https://github.com/theskumar/python-dotenv) and [.env](aws_lambda/.env) file. Additionally, this provides a good example of how to bundle the Lambda function with third party dependencies.


## Requirements:

 - [Terraform](https://www.terraform.io/downloads.html)
 - [AWS CLI tool](https://aws.amazon.com/cli/)
 - [Python 3.6+](https://www.python.org/downloads/)
 - [Make](https://www.gnu.org/software/make/)


## Setup

```bash
# create local Python virtual environment
python3 -m venv .venv
# activate virtual environment
. .venv/bin/activate
# install dependencies
pip install -r local.txt

# create credentials store and configure users
./passwd.py 
Welcome to the basic password manager.
Please enter your username:
vaidas
Please enter your password:
Password:


# configure AWS CLI credentials
aws configure

# set Terraform variables using .env file
make .env
# or
cp sample.env .env

# load .env values to the current environment
export $(cat .env| xargs)

# test lambda function
make test

# deploy the site
make deploy
```


## References
  - [Adding Authentication to Static Sites with AWS Lambda](https://douglasduhaime.com/posts/s3-lambda-auth.html)
  - [Tutorial: Creating a simple Lambda@Edge function](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/lambda-edge-how-it-works-tutorial.html)
  - [Lambda@Edge Design Best Practices](https://aws.amazon.com/blogs/networking-and-content-delivery/lambdaedge-design-best-practices/)
  - [Lambda@Edge event structure](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/lambda-event-structure.html)
  - [AWS Lambda context object in Python](https://docs.aws.amazon.com/lambda/latest/dg/python-context.html)
  - [Lambda@Edge example functions](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/lambda-examples.html)
  - [Creating AWS Lambda environment variables from AWS Secrets Manager](https://aws.amazon.com/blogs/compute/creating-aws-lambda-environmental-variables-from-aws-secrets-manager/)
  - [Restrictions on edge functions](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/edge-functions-restrictions.html)
  - [Redirect static websites on AWS with Lambda@Edge](https://medium.com/@robbytaylor/redirect-static-websites-on-aws-with-lambda-edge-14f2944ae02d)
  - [Uploading Multiple files in AWS S3 from terraform](https://stackoverflow.com/questions/57456167/uploading-multiple-files-in-aws-s3-from-terraform)
  - [Deploy Python Lambda functions with .zip file archives](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html)
  - [CodePen: CSS Mars Landing](https://codepen.io/mgitch/pen/pECcD)
  - [How To Hash Passwords In Python](https://nitratine.net/blog/post/how-to-hash-passwords-in-python/)
