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
            INSERT INTO SubstanceUse (
                student_id, 
                HOMETYPE_N, 
                COLLEGE, 
                ArmedForcesReservesOrNationalGuard, 
                SCH_SUSP_ALDRG, 
                NumberOfTimesArrestedValue, 
                USUAL_DOC, 
                KNOW_SA, 
                KNOW_HIV, 
                ParoleOrProbation, 
                HINCOMEO_N, 
                30daystext, 
                VAP30D, 
                ANYTOB30D, 
                MJ30D, 
                DaysUsedPrescriptionOpioidDrugsNumber, 
                DaysUsedOtherPrescriptionDrugsNumber, 
                DaysUsedNonPrescriptionOpioidDrugsNumber, 
                ILL30D, 
                INJECT30D, 
                DaysShareInjectionEquipmentNumber, 
                ALC30D, 
                BINGE530D, 
                THRIVE1, 
                THRIVE2, 
                THRIVE3, 
                THRIVE4, 
                THRIVE5, 
                THRIVE6, 
                THRIVE7, 
                THRIVE8, 
                THRIVE9, 
                4WKSLARGESTSD, 
                DRINKSBYHOUR, 
                BACHEIGHT, 
                BACWEIGHT
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s
            )
        """, (
            data['student_id'], 
            data['HOMETYPE_N'], 
            data['COLLEGE'], 
            data['ArmedForcesReservesOrNationalGuard'], 
            data['SCH_SUSP_ALDRG'], 
            data['NumberOfTimesArrestedValue'], 
            data['USUAL_DOC'], 
            data['KNOW_SA'], 
            data['KNOW_HIV'], 
            data['ParoleOrProbation'], 
            data['HINCOMEO_N'], 
            data['_30daystext'], 
            data['VAP30D'], 
            data['ANYTOB30D'], 
            data['MJ30D'], 
            data['DaysUsedPrescriptionOpioidDrugsNumber'], 
            data['DaysUsedOtherPrescriptionDrugsNumber'], 
            data['DaysUsedNonPrescriptionOpioidDrugsNumber'], 
            data['ILL30D'], 
            data['INJECT30D'], 
            data['DaysShareInjectionEquipmentNumber'], 
            data['ALC30D'], 
            data['BINGE530D'], 
            data['THRIVE1'], 
            data['THRIVE2'], 
            data['THRIVE3'], 
            data['THRIVE4'], 
            data['THRIVE5'], 
            data['THRIVE6'], 
            data['THRIVE7'], 
            data['THRIVE8'], 
            data['THRIVE9'], 
            data['_4WKSLARGESTSD'], 
            data['DRINKSBYHOUR'], 
            data['BACHEIGHT'], 
            data['BACWEIGHT']
        ))
    conn.commit()

    cursor.execute("UPDATE Student SET dob = %s, gender = %s, section1_flag = %s WHERE student_id = %s", (data['dob'], data['gender'], 1, data['student_id']))
    conn.commit()

            
    cursor.close()
    conn.close()

    return {
                "statusCode": 200,
                "body": json.dumps({"message": "Data inserted successfully"})
            }