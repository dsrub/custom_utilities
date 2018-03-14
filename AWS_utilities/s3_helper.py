import os
import boto3
import pandas as pd
import io

class S3_helper(object):
	""" Some tools for reading/writing data from/to S3

	Parameters
	------------
	AWS_ACCESS_KEY_ID : str
		AWS key 
	AWS_SECRET_ACCESS_KEY : str
		AWS secret access key


	"""
	def __init__(self, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY):
		os.environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY_ID
		os.environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY

	def read_df(self, bucket, key, *args, **kwargs):
		""" Read and return a pandas dataframe from an S3 bucket
	
		Parameters
		------------
		bucket : str
			S3 bucket (e.g.: "vmn.doug")
		key : str
			path in bucket containing the data 
			(e.g.: "identify_neilsen_pids/pid_market_breaks_000.gz")
		*args:
			Arguments to be passed to pandas' read_csv
		**kwargs:
			Keyword arguments to be passed to pandas' read_csv

		Returns
		------------
		A pandas dataframe

		"""

		s3_client = boto3.client('s3')
		obj = s3_client.get_object(Bucket=bucket, Key=key)

		return pd.read_csv(io.BytesIO(obj['Body'].read()), *args, **kwargs)

	def read_file(self, bucket, key, parse=False, delimiter=None):
		""" Read and return a file from an S3 buckey
	
		Parameters
		------------
		bucket : str
			S3 bucket (e.g.: "vmn.doug")
		key : str
			path in bucket containing the data 
			(e.g.: "identify_neilsen_pids/data.txt")
		parse : bool
			If false, returns contents of file as a single string.  If true,
			parses the string by the supplied delimiter and returns a list of
			strings. Default is False.
		delimiter : str
			Default is None.  Must stupply if parse=True.

		Returns
		------------
		The data as a single string if parse=False, and as a list if parse=True.

		"""
		s3 = boto3.resource('s3')
		bucket = s3.Bucket(bucket)

		for obj in bucket.objects.all():
			key_obj = obj.key
			if key_obj == key:
				body = obj.get()['Body'].read()
		if parse:
			return body.decode("utf-8").split(delimiter)
		else:
			return body.decode("utf-8")




