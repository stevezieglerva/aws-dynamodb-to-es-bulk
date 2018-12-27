import unittest
import time
import boto3
from lambda_function import *
import json
from S3TextFromLambdaEvent import *

event_one_file = {"Records": [
		{"eventID": "30356c817fedcb80d47f7048016efb6c", "eventName": "INSERT", "eventVersion": "1.1", "eventSource": "aws:dynamodb", "awsRegion": "us-east-1", "dynamodb": {"ApproximateCreationDateTime": 1545917438.0, "Keys": {"key_indicator": {"S": "event_1545917438.223041"
					}
				}, "NewImage": {"timestamp_local": {"S": "2018-12-27 08: 30: 38.279223-05: 00"
					}, "event": {"S": "{\"_index\": \"aws_code_index\",	\"_id\": \"\",\"data\": {\"lambda_name\": \"super_lambda\",	\"@timestamp\": \"2018-12-27T13:30:20.473\"		}		}"
					}, "key_indicator": {"S": "event_1545917438.223041"
					}, "ttl": {"N": "1545917438.279223"
					}, "timestamp": {"S": "2018-12-27 13: 30: 38.279223+00: 00"
					}
				}, "SequenceNumber": "5848700000000000985340818", "SizeBytes": 1784, "StreamViewType": "NEW_IMAGE"
			}, "eventSourceARN": "arn:aws:dynamodb:us-east-1: 112280397275:table/elasticsearch-queue/stream/2018-12-27T13: 13: 11.209"
		}
	]
}

class TestMethods(unittest.TestCase):

	def test_lambda_function__two_file_event__successful_results(self):
		# Arrange

		# Act
		result = lambda_handler(event_one_file, None)
		print(json.dumps(result, indent=3))

		# Assert
		self.assertEqual(result["msg"], "Success")
		self.assertEqual(result["events_to_process"], 1)


if __name__ == '__main__':
	unittest.main()		


