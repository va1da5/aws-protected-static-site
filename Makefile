include .env
export

.PHONY: help
help:
	@echo "Usage: make [options]"
	@echo "Options:"
	@echo "		help                   - this message"
	@echo "		lambda                 - bundle lambda function"
	@echo "		test                   - unit test the lambda function"
	@echo "		deploy                 - deploy the static site and lambda function"


.PHONY: clean
clean:
	@rm -rf dist
	@rm -rf terraform/.terraform

dist:
	@mkdir dist

.PHONY: lambda
lambda: clean dist
	@cd ./aws_lambda; zip -ur9 ../dist/lambda.zip * .[^.]*;\
		cd ..; pip install -r requirements.txt --target ./dist/packages;\
		cd ./dist/packages/;\
		zip -ur9 ../../dist/lambda.zip *;

lambda/.passwd:
	@touch lambda/.passwd


terraform/.terraform:
	@cd terraform; terraform init;


.PHONY: deploy
deploy: lambda terraform/.terraform
	@cd terraform; terraform plan; terraform apply -auto-approve;


.PHONY: plan
plan: lambda terraform/.terraform
	@cd terraform; terraform plan

.PHONY: test
test:
	@. .venv/bin/activate; pytest


.PHONY: destroy
destroy:
	@cd terraform; terraform destroy


.env:
	@cp sample.env .env

