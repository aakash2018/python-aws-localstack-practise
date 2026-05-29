import boto3, json

# LocalStack endpoint पर IAM client बनाओ
iam = boto3.client("iam", endpoint_url="http://localhost:4566")
print(iam.list_users())  # IAM users की लिस्ट दिखाओ

# 1. User Create
# user = iam.create_user(UserName="aakash-user")
# print("User Created:", user["User"]["UserName"])

# 2. Users List
users = iam.list_users()
print("Users List:", users["Users"])

# 3. Specific User Details
user_details = iam.get_user(UserName="admin")
print("User Details:", user_details["User"])

# 4. Group Create
# group = iam.create_group(GroupName="aakash-developers")
# print("Group Created:", group["Group"]["GroupName"])

# 5. User Add to Group
iam.add_user_to_group(UserName="admin", GroupName="aakash-developers")
print("User added to group aakash-developers")

# 6. Roles List
roles = iam.list_roles()
print("Roles:", roles["Roles"])

# 7. IAM Groups List
groups = iam.list_groups()
print("Groups:", groups["Groups"])

# 8. Role Create (trust-policy.json से)
trust_policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {"Service": "ec2.amazonaws.com"},
        "Action": "sts:AssumeRole"
    }]
}

# role = iam.create_role(
#     RoleName="EC2Role-aakash",
#     AssumeRolePolicyDocument=json.dumps(trust_policy)
# )
# print("Role Created:", role["Role"]["RoleName"])

# 9. Verify Roles
roles = iam.list_roles()
for r in roles["Roles"]:
    print("Role:", r["RoleName"])

