data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    actions = [
      "sts:AssumeRole",
    ]

    principals {
      type = "Service"
      identifiers = [
        "edgelambda.amazonaws.com",
        "lambda.amazonaws.com",
      ]
    }

    effect = "Allow"
  }
}

data "aws_iam_policy_document" "lambda_log_access" {

  statement {
    actions = [
      "logs:*",
    ]

    resources = [
      "arn:aws:logs:*:*:*",
    ]

    effect = "Allow"
  }

  statement {
    actions = [
      "s3:GetObject",
      "s3:PutObject",
    ]

    resources = [
      "arn:aws:s3:::*",
    ]

    effect = "Allow"
  }
}


resource "aws_iam_role" "lambda" {
  name               = "LambdaRole-${var.lambda_function_name}"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

resource "aws_iam_role_policy_attachment" "lambda_log_access" {
  role       = aws_iam_role.lambda.name
  policy_arn = aws_iam_policy.lambda_log_access.arn
}


resource "aws_iam_policy" "lambda_log_access" {
  name   = "LambdaLogAccess-${var.lambda_function_name}"
  policy = data.aws_iam_policy_document.lambda_log_access.json
}

resource "null_resource" "make_lambda" {

  provisioner "local-exec" {
    command = "cd ..; make lambda"
  }
}

resource "aws_lambda_function" "lambda" {
  filename         = "../dist/lambda.zip"
  function_name    = var.lambda_function_name
  role             = aws_iam_role.lambda.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.9"
  publish          = true
  source_code_hash = filebase64sha256("../dist/lambda.zip")

  depends_on = [null_resource.make_lambda]
}
