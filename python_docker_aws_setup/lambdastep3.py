def lambda_handler(event, context):
    return {"message": "done", "order_id": event["order_id"]}