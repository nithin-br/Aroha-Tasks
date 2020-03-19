import os
from io import StringIO
from io import BytesIO
import pandas as pd
import cx_Oracle
import xlsxwriter
import boto3
from botocore.exceptions import NoCredentialsError

# accessing the aws credentials from environment variables
access_key = os.environ.get('aws_access_key1')
secret_key = os.environ.get('aws_secret_key1')

# credentials for oracle rds
host_name = 'aroha-dev.ciazrzpzwsik.ap-south-1.rds.amazonaws.com'
user_name = 'testuser'
pwd = 'testuser'
service_name = 'ORCL'

# establishing connection with the aws oracle rds
connection = cx_Oracle.connect(str.format('{0}/{1}@{2}/{3}', user_name, pwd, host_name, service_name))
cursor = connection.cursor()

# fetch data
query = "SELECT * FROM users"
fetch_data = pd.read_sql(query, connection)

'''writing this table to a csv file and xlsx file.this is written/read as in-memory file object using the 
stringio and bytesio'''

# to csv
with StringIO() as csv_buffer:
    fetch_data.to_csv(csv_buffer, index=False)
    data_csv = csv_buffer.getvalue()
# to xlsx
with BytesIO() as xl_buffer:
    fetch_data.to_excel(xl_buffer, index=False, engine='xlsxwriter')
    data_xls = xl_buffer.getvalue()

# function to upload to s3
def upload_to_aws(in_memory_file, bucket_name, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key, region_name='ap-south-1')

    try:
        s3.put_object(Bucket=bucket_name,
                      Body=in_memory_file,
                      Key=s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


# upload file in s3 bucket
uploaded_1 = upload_to_aws(data_csv, 'myfirstbucket14', 'china_navig/sample_table.csv')
uploaded_2 = upload_to_aws(data_xls, 'myfirstbucket14', 'china_navig/sample_table.xlsx')
