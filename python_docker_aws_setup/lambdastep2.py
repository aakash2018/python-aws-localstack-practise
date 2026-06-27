def lambda_handler(event, context):
    return {"order_id": event["order_id"], "payment": "success"}