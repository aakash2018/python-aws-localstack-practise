import boto3
import subprocess

# LocalStack endpoint
endpoint = "http://localhost:4566"

# 1. ECR Client
ecr = boto3.client("ecr", region_name="us-east-1", endpoint_url=endpoint)

# 2. Create Repository
repo_name = "fastapi-setup"
# response = ecr.create_repository(repositoryName=repo_name)
# print("Repository Created:", response["repository"]["repositoryName"])

# 3. List Repositories
repos = ecr.describe_repositories()
for r in repos["repositories"]:
    print("Repo:", r["repositoryName"], "URI:", r["repositoryUri"])

# 4. Get Repository URI
repo_uri = repos["repositories"][0]["repositoryUri"]
print("Repository URI:", repo_uri)

# 5. Docker Build
try:
    subprocess.run(["docker", "build", "-t", "./fastapi-setup:v1",  "-f", ".dockerfile", "."], check=True)
except subprocess.CalledProcessError as e:
    print("Error code:", e.returncode)
    print("Error output:", e.stderr)

# subprocess.run(["docker", "build", "-t", "fastapi-setup:v1", "."])

# 6. Docker Tag
subprocess.run(["docker", "tag", "fastapi-setup:v1", f"{repo_uri}:v1"], check=True)

# 7. Docker Push
subprocess.run(["docker", "push", f"{repo_uri}:v1"], check=True)

# 8. Verify Image in ECR
images = ecr.list_images(repositoryName=repo_name)
print("Images in ECR:", images["imageIds"])
