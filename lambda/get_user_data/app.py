import json
import logging
import os
import sys
import mysql.connector


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configuration
conn = mysql.connector.connect(
    host=os.environ.get('DB_HOSTNAME'),
    port=os.environ.get('DB_PORT_NUMBER'),
    user= os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    database=os.environ.get('DB_DATABASE')
)

# Database Connection
cursor = conn.cursor()

def lambda_handler(event, context):

    params = json.loads(event['body'])

    name = params['name']
    id = params['id']

    cursor.execute("SELECT student_id,section1_flag FROM Student WHERE id = %s and name = %s order by created_at desc", (id,name))
    data = cursor.fetchall()

    if data:
        section1_flag = data[0][1]
        # You can further process the data or directly return it
        response = {
            "statusCode": 200,
            "body": json.dumps({"section1_flag": section1_flag,
                                "student_id": data[0][0]})
        }
    else:
        # Data not found
        response = {
            "statusCode": 404,
            "body": json.dumps({"error": "Data not found"})
        }