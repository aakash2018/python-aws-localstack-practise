import boto3
import json

# LocalStack endpoint
endpoint_url = "http://localhost:4566"

# 1. Lambda Client
lambda_client = boto3.client("lambda", endpoint_url=endpoint_url, region_name="us-east-1")

# 2. IAM Client
iam_client = boto3.client("iam", endpoint_url=endpoint_url, region_name="us-east-1")

# Step 3: Trust Policy बनाओ
trust_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }
    ]
}

# Step 4: IAM Role Create
# role = iam_client.create_role(
#     RoleName="lambda-role",
#     AssumeRolePolicyDocument=json.dumps(trust_policy)
# )
# print("Role Created:", role["Role"]["Arn"])

# Step 5: Lambda Function Create
# with open("lambda.zip", "rb") as f:
#     zipped_code = f.read()

# response = lambda_client.create_function(
#     FunctionName="hello-lambda",
#     Runtime="python3.12",
#     Role=role["Role"]["Arn"],
#     Handler="lambdafunction.lambda_handler",
#     Code={"ZipFile": zipped_code},
# )
# print("Lambda Created:", response["FunctionArn"])

# Step 6: Verify Functions
functions = lambda_client.list_functions()
print("Functions:=>", functions)

# Step 7: Invoke Lambda (without event)
resp = lambda_client.invoke(FunctionName="hello-lambda")
print("Response:=>", resp["Payload"].read().decode())

# Step 9–11: Update Lambda Code
with open("lambda.zip", "rb") as f:
    new_code = f.read()

update_resp = lambda_client.update_function_code(
    FunctionName="hello-lambda",
    ZipFile=new_code
)
print("Updated Function:", update_resp)

# Step 13: Invoke Lambda with Event
event = {"name": "Aakash"}
resp = lambda_client.invoke(
    FunctionName="hello-lambda",
    Payload=json.dumps(event)
)
print("Response with Event:", resp["Payload"].read().decode())
