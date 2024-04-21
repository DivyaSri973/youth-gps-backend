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
    print(event)

    body = json.loads(event['body'])
    data = body.get('data')


    cursor.execute("""
        INSERT INTO SexualHealth (
            student_id,
            id,
            created_at,
            yaacq_1,
            yaacq_2,
            yaacq_3,
            yaacq_4,
            yaacq_5,
            yaacq_6,
            yaacq_7,
            yaacq_8,
            yaacq_9,
            yaacq_10,
            yaacq_11,
            yaacq_12,
            yaacq_13,
            yaacq_14,
            yaacq_15,
            yaacq_16,
            yaacq_17,
            yaacq_18,
            yaacq_19,
            yaacq_20,
            yaacq_21,
            yaacq_22,
            yaacq_23,
            yaacq_24,
            YOUTH_SEXPARTNERS,
            YOUTH_UNPSEX,
            SEXPARTNERS,
            _30D_partnertext,
            PARTNER_MALE,
            PARTNER_FEMALE,
            PARTNER_TRANS,
            PARTNER_MONO,
            PARTNER_MULTI,
            PARTNER_HIV,
            PARTNER_HCV,
            PARTNER_PWID,
            PARTNER_MSM,
            SEXFORRESOURCES,
            SEXACT3_SF,
            SEXACT4_SF,
            KNOW_HIV,
            RSKANYSEX_UNP,
            RSKSEX_ALCDRG,
            RiskOfHarmWhenUsingTobaccoOnceOrTwiceWeek,
            RSKALC,
            RSKMJ,
            RSKNDL_SHR,
            RSKNDL_INJECT,
            RiskOfHarmWhenUsingNonPrescriptionOpioidDrugsOnceOrTwiceWeek,
            RiskOfHarmWhenUsingPrescriptionOpioidDrugsOnceOrTwiceWeek,
            ANYABUSE_3M,
            CNTRL_REFUSECNDM,
            CNTRL_ALC,
            CNTRL_DRG,
            THRIVE10,
            THRIVE11,
            THRIVE12,
            THRIVE13,
            THRIVE14,
            THRIVE15,
            THRIVE16,
            THRIVE17
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s
        )
    """, (
        data['student_id'],
        data['id'],
        data['created_at'],
        data['yaacq_1'],
        data['yaacq_2'],
        data['yaacq_3'],
        data['yaacq_4'],
        data['yaacq_5'],
        data['yaacq_6'],
        data['yaacq_7'],
        data['yaacq_8'],
        data['yaacq_9'],
        data['yaacq_10'],
        data['yaacq_11'],
        data['yaacq_12'],
        data['yaacq_13'],
        data['yaacq_14'],
        data['yaacq_15'],
        data['yaacq_16'],
        data['yaacq_17'],
        data['yaacq_18'],
        data['yaacq_19'],
        data['yaacq_20'],
        data['yaacq_21'],
        data['yaacq_22'],
        data['yaacq_23'],
        data['yaacq_24'],
        data['YOUTH_SEXPARTNERS'],
        data['YOUTH_UNPSEX'],
        data['SEXPARTNERS'],
        data['_30D_partnertext'],
        data['PARTNER_MALE'],
        data['PARTNER_FEMALE'],
        data['PARTNER_TRANS'],
        data['PARTNER_MONO'],
        data['PARTNER_MULTI'],
        data['PARTNER_HIV'],
        data['PARTNER_HCV'],
        data['PARTNER_PWID'],
        data['PARTNER_MSM'],
        data['SEXFORRESOURCES'],
        data['SEXACT3_SF'],
        data['SEXACT4_SF'],
        data['KNOW_HIV'],
        data['RSKANYSEX_UNP'],
        data['RSKSEX_ALCDRG'],
        data['RiskOfHarmWhenUsingTobaccoOnceOrTwiceWeek'],
        data['RSKALC'],
        data['RSKMJ'],
        data['RSKNDL_SHR'],
        data['RSKNDL_INJECT'],
        data['RiskOfHarmWhenUsingNonPrescriptionOpioidDrugsOnceOrTwiceWeek'],
        data['RiskOfHarmWhenUsingPrescriptionOpioidDrugsOnceOrTwiceWeek'],
        data['ANYABUSE_3M'],
        data['CNTRL_REFUSECNDM'],
        data['CNTRL_ALC'],
        data['CNTRL_DRG'],
        data['THRIVE10'],
        data['THRIVE11'],
        data['THRIVE12'],
        data['THRIVE13'],
        data['THRIVE14'],
        data['THRIVE15'],
        data['THRIVE16'],
        data['THRIVE17']
    ))

    conn.commit()

    cursor.execute("UPDATE Student SET section1_flag = %s WHERE student_id = %s", ( 0, data['student_id']))
    conn.commit()

            
    cursor.close()
    conn.close()

    return {
                "statusCode": 200,
                "body": json.dumps({"message": "Data inserted successfully"})
            }