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

    cursor.execute("SELECT ANYTOB30D, VAP30D, MJ30D, ALC30D, THRIVE1, BINGE530D, 4WKSLARGESTSD, DRINKSBYHOUR, BACWEIGHT, THRIVE2, THRIVE3, THRIVE4, THRIVE5, THRIVE6, THRIVE7, THRIVE8, THRIVE9 FROM SubstanceUse WHERE student_id = %s order by created_at desc limit 1", (id))
    data = cursor.fetchall()

    if data:

        metrics = {}
        metrics['ANYTOB30D'] = data[0][0] if data[0][0] else 0
        if data[0][1] > 9:
            metrics['VAP30D'] = data[0][1]
            metrics['show_vape_comparision'] = 1
        elif data[0][1] <= 9 and data[0][1] != 0:
            metrics['VAP30D'] = data[0][1]
            metrics['show_vape_comparision'] = 0
        else:
            metrics['VAP30D'] = 0
            metrics['show_vape_comparision'] = 0
        
        if data[0][2] > 4:
            metrics['MJ30D'] = data[0][2]
            metrics['show_mj_comparision'] = 1
        elif data[0][2] <= 4 and data[0][2] != 0:
            metrics['MJ30D'] = data[0][2]
            metrics['show_mj_comparision'] = 0
        else:
            metrics['MJ30D'] = 0
            metrics['show_mj_comparision'] = 0

        if data[0][3] >= 4 and data[0][3] <= 7:
            metrics['ALC30D'] = data[0][3]
            metrics['show_alc_comparision'] = 1
            metrics['show_drinker_pop_avg'] = 0
        elif data[0][3] > 7:
            metrics['ALC30D'] = data[0][3]
            metrics['show_alc_comparision'] = 1
            metrics['show_drinker_pop_avg'] = 1
        elif data[0][3] < 4 and data[0][3] != 0:
            metrics['ALC30D'] = data[0][3]
            metrics['show_alc_comparision'] = 0
            metrics['show_drinker_pop_avg'] = 0
        else:  
            metrics['ALC30D'] = 0
            metrics['show_alc_comparision'] = 0
            metrics['show_drinker_pop_avg'] = 0

        if data[0][4] > 3.5:
            metrics['ALOCHOL_QUANTITY'] = data[0][4]
            metrics['show_alcohol_quantity_comparision'] = 1
            metrics['show_drinker_pop_avg_alcohol_quantity'] = 1
        elif data[0][4] <= 3.5 and data[0][4] != 0:
            metrics['ALOCHOL_QUANTITY'] = data[0][4]
            metrics['show_alcohol_quantity_comparision'] = 0
            metrics['show_drinker_pop_avg_alcohol_quantity'] = 0
        else:
            metrics['ALOCHOL_QUANTITY'] = 0
            metrics['show_alcohol_quantity_comparision'] = 0
            metrics['show_drinker_pop_avg_alcohol_quantity'] = 0
        
        if data[0][5] >= 4:
            metrics['BINGE530D'] = data[0][5]
            metrics['show_binge_comparision'] = 1
            metrics['show_drinker_pop_avg_binge'] = 1
        elif data[0][5] < 4 and data[0][5] != 0:
            metrics['BINGE530D'] = data[0][5]
            metrics['show_binge_comparision'] = 0
            metrics['show_drinker_pop_avg_binge'] = 0
        else:   
            metrics['BINGE530D'] = 0
            metrics['show_binge_comparision'] = 0
            metrics['show_drinker_pop_avg_binge'] = 0
        
        BAC = 0
        no_standard_drinks = data[0][6] if data[0][8] else 0
        gender_data = cursor.execute("SELECT gender from Student where student_id = %s", (id)).fetchall()
        if gender_data:
            gender = gender_data[0][0]
        else:
            gender = 'M'
        if gender == 'M':
            sex_constant = 7.5
        else:
            sex_constant = 9
        
        no_of_drinks_per_hour = data[0][7] if data[0][7] else 0
        weight = data[0][8] if data[0][8] else 0
        BAC = ((no_standard_drinks / 14) * (weight * sex_constant)) - (no_of_drinks_per_hour * 0.016)
        metrics['BAC'] = BAC

        if BAC > 0.04:
            metrics['show_bac_comparision'] = 1
        elif BAC <= 0.04 and BAC != 0:
            metrics['show_bac_comparision'] = 0

        
        audit_score = 0 

        if data[0][9]:
            audit_score += data[0][9]
        if data[0][10]:
            audit_score += data[0][10]
        if data[0][11]:
            audit_score += data[0][11]
        if data[0][12]:
            audit_score += data[0][12]
        if data[0][13]:
            audit_score += data[0][13]
        if data[0][14]:
            audit_score += data[0][14]
        if data[0][15]:
            audit_score += data[0][15]


        if data[0][16]:
            audit_score += data[0][16] if data[0][16] else 0
        
        if audit_score > 0:
            standard = data[0][4] / audit_score

            if standard <= 2:
                metrics['audit_score'] = audit_score
            elif standard > 2 and standard <= 4:
                metrics['audit_score'] = audit_score + 1
            elif standard > 4 and standard <= 6:
                metrics['audit_score'] = audit_score + 2
            elif standard > 6 and standard < 10:
                metrics['audit_score'] = audit_score + 3
            elif standard >= 10:
                metrics['audit_score'] = audit_score + 4

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