import boto3
import time
import datetime
import logging
import structlog
import os
import json
from S3TextFromLambdaEvent import *
from Event import *


def lambda_handler(event, context):
	try:
		aws_request_id = ""
		if context is not None:
			aws_request_id = context.aws_request_id

		print("Started")
		if "text_logging" in os.environ:
			log = structlog.get_logger()
		else:
			log = setup_logging("aws-code-index-dynamodb-to-es-bulk", event, aws_request_id)

		count = 0
		dynamo_records_to_process = []
		for event in event["Records"]:
			if event["eventName"] == "INSERT":
				key_indicator = event["dynamodb"]["Keys"]["key_indicator"]["S"]
				count = count + 1
				print(str(count) + " - Found: " + key_indicator)
				dynamo_records_to_process.append(key_indicator)


		log.critical("finished")
		print("Finished")

	except Exception as e:
		print("Exception: "+ str(e))
		raise(e)

	return {"msg" :  "Success", "events_to_process" : count}




def setup_logging(lambda_name, lambda_event, aws_request_id):
	logging.basicConfig(
		format="%(message)s",
		stream=sys.stdout,
		level=logging.INFO
	)
	structlog.configure(
		processors=[
			structlog.stdlib.filter_by_level,
			structlog.stdlib.add_logger_name,
			structlog.stdlib.add_log_level,
			structlog.stdlib.PositionalArgumentsFormatter(),
			structlog.processors.TimeStamper(fmt="iso"),
			structlog.processors.StackInfoRenderer(),
			structlog.processors.format_exc_info,
			structlog.processors.UnicodeDecoder(),
			structlog.processors.JSONRenderer()
		],
		context_class=dict,
		logger_factory=structlog.stdlib.LoggerFactory(),
		wrapper_class=structlog.stdlib.BoundLogger,
		cache_logger_on_first_use=True,
	)

	log = structlog.get_logger()
	log = log.bind(aws_request_id=aws_request_id)
	log.critical("started", input_events=json.dumps(lambda_event, indent=3))

	return log

	