variable "region" {
  type        = string
  default     = "us-east-1"
  description = "The region to deploy the S3 bucket into"
}

variable tags {
  type        = map
  default     = {}
  description = "Tags to label resources with"
}

variable "bucket_name" {
  type        = string
  default     = "my-awesome-static-site"
  description = "The name of the bucket"
}

variable "lambda_function_name" {
  type        = string
  default     = "cloudfront-basic-auth"
  description = "The name of the Lambda@Edge function for redirecting to the primary hostname"
}

variable cloudfront_default_root_object {
  type        = string
  default     = "index.html"
  description = "The default root object of the Cloudfront distribution"
}

variable cloudfront_price_class {
  type        = string
  default     = "PriceClass_All"
  description = "Cloudfront price classes: `PriceClass_All`, `PriceClass_200`, `PriceClass_100`"
}

variable cloudfront_aliases {
  type        = list
  default     = []
  description = "List of FQDNs to be used as alternative domain names (CNAMES) for Cloudfront"
}

