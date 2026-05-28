import boto3

# Point to LocalStack
s3 = boto3.client("s3", endpoint_url="http://localhost:4566")


# Create a bucket
s3.create_bucket(Bucket="my-test-bucket")

# Upload file
s3.put_object(Bucket="my-test-bucket", Key="comments.txt", Body="Hello LocalStack!")

resp = s3.list_objects(Bucket="my-test-bucket")
print(resp)
