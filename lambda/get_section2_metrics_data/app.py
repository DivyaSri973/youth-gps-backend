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
    id = params['student_id']

    cursor.execute("SELECT YOUTH_SEXPARTNERS, SEXACT3_SF, KNOW_HIV, RSKANYSEX_UNP, RSKSEX_ALCDRG, RiskOfHarmWhenUsingTobaccoOnceOrTwiceWeek, RSKALC, RSKMJ, RSKNDL_SHR, RSKNDL_INJECT, RiskOfHarmWhenUsingNonPrescriptionOpioidDrugsOnceOrTwiceWeek, RiskOfHarmWhenUsingPrescriptionOpioidDrugsOnceOrTwiceWeek, RSKANYSEX_UNP, RSKSEX_ALCDRG, ANYABUSE_3M  FROM SexualHealth WHERE student_id = %s order by created_at desc limit 1", (id))
    data = cursor.fetchall()

    if data:

        metrics = {}
        if data[0][0] is not None:
            if data[0][0] < 2:
                metrics['YOUTH_SEXPARTNERS'] = 2
            else:
                metrics['YOUTH_SEXPARTNERS'] = data[0][0]
        else:
            metrics['YOUTH_SEXPARTNERS'] = 0

        if data[0][1] is not None:
            if data[0][1] > 4:
                metrics['SEXACT3_SF'] = data[0][1]
                metrics['DrinkingBeforeSex'] = 4.4
                metrics['AlcoholRelatedSexualConsequences'] = 7
            else:
                metrics['SEXACT3_SF'] = data[0][1]
                metrics['DrinkingBeforeSex'] = 0
                metrics['AlcoholRelatedSexualConsequences'] = 0
        else:
            metrics['SEXACT3_SF'] = 0
            metrics['DrinkingBeforeSex'] = 0
            metrics['AlcoholRelatedSexualConsequences'] = 0

        metrics['KNOW_HIV'] = data[0][2]
        flag = 0
        risk1 = data[0][3]
        risk2 = data[0][4]
        risk3 = data[0][5]
        risk4 = data[0][6]
        risk5 = data[0][7]
        risk6 = data[0][8]
        risk7 = data[0][9]
        risk8 = data[0][10]
        risk9 = data[0][11]
        risk10 = data[0][12]
        risk11 = data[0][13]
        if risk1 > 0 and risk1 <= 2:
            flag = 1
        if risk2 > 0 and risk2 <= 2:
            flag = 1
        if risk3 > 0 and risk3 <= 2:
            flag = 1
        if risk4 > 0 and risk4 <= 2:
            flag = 1
        if risk5 > 0 and risk5 <= 2:
            flag = 1
        if risk6 > 0 and risk6 <= 2:
            flag = 1
        if risk7 > 0 and risk7 <= 2:
            flag = 1
        if risk8 > 0 and risk8 <= 2:
            flag = 1
        if risk9 > 0 and risk9 <= 2:
            flag = 1
        if risk10 > 0 and risk10 <= 2:
            flag = 1
        if risk11 > 0 and risk11 <= 2:
            flag = 1
        metrics['RISK_FLAG'] = flag
        abuse = data[0][14]
        if abuse > 1:
            metrics['ABUSE_FLAG'] = 1
        else:
            metrics['ABUSE_FLAG'] = 0

        # You can further process the data or directly return it
        response = {
            "statusCode": 200,
            "body": json.dumps({"metrics": metrics,
                                "student_id": data[0][0]})
        }
    else:
        # Data not found
        response = {
            "statusCode": 404,
            "body": json.dumps({"error": "Data not found"})
        }