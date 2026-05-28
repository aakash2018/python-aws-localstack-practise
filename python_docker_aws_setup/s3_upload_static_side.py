import boto3
import os
import mimetypes

# LocalStack endpoint
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566"
)


# Step 1 — Bucket Create
bucket_name = "my-static-site"
s3.create_bucket(Bucket=bucket_name)

print("✅ Bucket created:", bucket_name)

folder_path = "./highfashion"

for root, dirs, files in os.walk(folder_path):
    for file in files:
        local_path = os.path.join(root, file)
        relative_path = os.path.relpath(local_path, folder_path)
        relative_path = relative_path.replace("\\", "/")
        content_type, _ = mimetypes.guess_type(local_path)
        extra_args = {"ACL": "public-read"}
        if content_type:
            extra_args["ContentType"] = content_type 
        s3.upload_file(
            local_path,
            bucket_name,
            relative_path,
            ExtraArgs=extra_args  # same as --acl public-read
        )
        print("📤 Uploaded:", relative_path)

# Step 3 — Website Hosting Enable
website_config = {
    "IndexDocument": {"Suffix": "index.html"},
    "ErrorDocument": {"Key": "error.html"}  # optional
}
s3.put_bucket_website(Bucket=bucket_name, WebsiteConfiguration=website_config)
print("🌐 Website hosting enabled")

# Step 4 — Verify Files
resp = s3.list_objects_v2(Bucket=bucket_name)
for obj in resp.get("Contents", []):
    print("📄", obj["Key"])


print("👉 Open in browser: http://localhost:4566/my-static-site/index.html")




