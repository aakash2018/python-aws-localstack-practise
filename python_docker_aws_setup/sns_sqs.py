import boto3

#localstack endpoint
endpoint_url = "http://localhost:4566"

# SNS client
sns = boto3.client("sns", endpoint_url=endpoint_url, region_name="us-east-1")

# SQS client
sqs = boto3.client("sqs", endpoint_url=endpoint_url, region_name="us-east-1")

# 1. SNS Topic बनाओ
topic = sns.create_topic(Name="my-topic-1")
topic_arn = topic["TopicArn"]
print("Topic ARN:", topic_arn)

# 2. SQS Queue बनाओ
queue = sqs.create_queue(QueueName="my-queue")
queue_url = queue["QueueUrl"]
print("Queue URL:", queue_url)

# 3. Queue ARN निकालो
attrs = sqs.get_queue_attributes(
    QueueUrl=queue_url,
    AttributeNames=["QueueArn"]
)
queue_arn = attrs["Attributes"]["QueueArn"]
print("Queue ARN:", queue_arn)

# 4. SNS Topic को SQS Queue से subscribe करो
sns.subscribe(
    TopicArn=topic_arn,
    Protocol="sqs",
    Endpoint=queue_arn
)

# 5. Message publish करो
sns.publish(
    TopicArn=topic_arn,
    Message="Order Created"
)

# 6. Queue से message receive करो
messages = sqs.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=1,
    WaitTimeSeconds=2
)

print("Messages:", messages.get("Messages", []))
for msg in messages:
    print("Message ID:", msg["MessageId"])
    print("Body:", msg["Body"])