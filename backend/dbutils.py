import json
import random
import mysql.connector
import numpy as np

HOST = 'eu-cdbr-west-01.cleardb.com'
USER = 'b0e845e610b5e1'
PASSWORD = 'dd1eef7b'
DATABASE = 'heroku_14806ad62e1ed9f'


def connect():
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
        ssl_disabled=True
    )


def fetchlastSessionId():
    db = connect()
    cursor = db.cursor()

    query = """
        SELECT SESSION_ID FROM SESSION_DATA ORDER BY SESSION_ID DESC LIMIT 1;
    """
    try:
        cursor.execute(query)
        lastSessionId = cursor.fetchone()
    except:
        print('Error occurred while fetching last session id')
        return 'null'

    db.close()
    if (lastSessionId is not None):
        return str(lastSessionId[0])
    else:
        return '0'


def fetchLastToolId():
    db = connect()
    cursor = db.cursor()

    query = """
        SELECT ID FROM TOOL_DATA ORDER BY ID DESC LIMIT 1;
    """
    try:
        cursor.execute(query)
        toolId = cursor.fetchone()
    except:
        print('Error occurred while fetching last tool id')
        return 'null'

    db.close()
    return toolId[0]


def insertSessionData(data):
    db = connect()
    cursor = db.cursor()

    query = """SELECT SCENARIO, count(*)
               From session_data Where FINISHED='Y'
               Group By SCENARIO"""

    try:
        cursor.execute(query, ())
        scenarioDistribution = dict(cursor.fetchall())
    except:
        print('Error occurred while fetching scenario from session_data')
        return json.dumps({'success': False})

    if ('0' not in scenarioDistribution and '1' in scenarioDistribution):
        new_scenario = '0'
    elif ('0' in scenarioDistribution and '1' not in scenarioDistribution):
        new_scenario = '1'
    elif ('0' not in scenarioDistribution and '1' not in scenarioDistribution):
        new_scenario = str(round(random.random()))
    else:
        if (scenarioDistribution is not None):
            if (scenarioDistribution['0'] > scenarioDistribution['1']):
                new_scenario = '1'
            elif (scenarioDistribution['0'] < scenarioDistribution['1']):
                new_scenario = '0'
            else:
                new_scenario = str(round(random.random()))
        else:
            new_scenario = str(round(random.random()))

    query = """SELECT TASK_SCENARIO FROM SESSION_DATA Where FINISHED='Y' ORDER BY SESSION_ID DESC LIMIT 1;"""
    try:
        cursor.execute(query)
        task_scenario = cursor.fetchone()
    except:
        print('Error occurred while fetching task_scenario from session_data')
        return json.dumps({'success': False})

    if (task_scenario is not None):
        new_task_scenario = (task_scenario[0] + 1) % 6
    else:
        new_task_scenario = 0

    query = """INSERT INTO SESSION_DATA (SCENARIO, TASK_SCENARIO, SOURCE, OLD_PARTICIPANT, FINISHED) VALUES (%s, %s, %s, %s, %s)"""
    values = (new_scenario, new_task_scenario,
              data['source'], data['oldParticipant'], 'N')

    try:
        cursor.execute(query, values)
        db.commit()
    except:
        print('Error occurred while inserting data to session_data')
        return json.dumps({'success': False})

    db.close()
    return json.dumps({'success': True, 'SCENARIO': new_scenario, 'SESSION_ID': fetchlastSessionId(), 'TASK_SCENARIO': new_task_scenario}, indent=4)


def computePercentage(data):
    MAX_STD_DEVIATION = 2.36

    pred = np.array([data['best'], data['secondBest'],
                    data['thirdBest']], dtype=np.float32)
    # print(f'Predictions: {pred}')

    # Use classifer's prediction probability for confidence level
    # Use a single "most" accurate model based on validation set

    # Tranforming the mean value of predictions in the range [0, 5]
    # and changing the features from NOT

    # score = 5 - max(min(data['best'], 5), 0)
    # score = int(score * 20)
    score = 100 - int(data['best'] * 20)
    if score > 100:
        score = 100
    if score < 0:
        score = 0

    # standard deviation => uncertainty
    # 1 - standard deviation => certainty
    confidence = 100 - int((pred.std()/MAX_STD_DEVIATION) * 100)
    if confidence > 100:
        confidence = 100
    if confidence < 0:
        confidence = 0

    return {
        'value': score,
        'confidence': confidence
    }


def insertToolData(taskData, predictions):
    db = connect()
    cursor = db.cursor()

    aggregatePredictions = {
        'state1': computePercentage(predictions['state1_new']),
        'state3': computePercentage(predictions['state_3']),
        'state4': computePercentage(predictions['state_4']),
        'state5': computePercentage(predictions['state_5']),
        'state6': computePercentage(predictions['state_6']),
        'state7': computePercentage(predictions['state_7']),
        'state8': computePercentage(predictions['state_8']),
        'state9': computePercentage(predictions['state_9'])
    }

    query = """
        INSERT INTO TOOL_DATA (
            SESSION_ID,
            TITLE,
            DESCRIPTION,
            OVERALL_CLARITY_VALUE,
            OVERALL_CLARITY_CONFIDENCE,
            FEATURE1_VALUE,
            FEATURE2_VALUE,
            FEATURE3_VALUE,
            FEATURE4_VALUE,
            FEATURE5_VALUE,
            FEATURE6_VALUE,
            FEATURE7_VALUE,
            FEATURE1_CONFIDENCE,
            FEATURE2_CONFIDENCE,
            FEATURE3_CONFIDENCE,
            FEATURE4_CONFIDENCE,
            FEATURE5_CONFIDENCE,
            FEATURE6_CONFIDENCE,
            FEATURE7_CONFIDENCE)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    values = (
        int(taskData['sessionId']),
        taskData['title'],
        taskData['description'],
        aggregatePredictions['state1']['value'],
        aggregatePredictions['state1']['confidence'],
        aggregatePredictions['state3']['value'],
        aggregatePredictions['state4']['value'],
        aggregatePredictions['state5']['value'],
        aggregatePredictions['state6']['value'],
        aggregatePredictions['state7']['value'],
        aggregatePredictions['state8']['value'],
        aggregatePredictions['state9']['value'],
        aggregatePredictions['state3']['confidence'],
        aggregatePredictions['state4']['confidence'],
        aggregatePredictions['state5']['confidence'],
        aggregatePredictions['state6']['confidence'],
        aggregatePredictions['state7']['confidence'],
        aggregatePredictions['state8']['confidence'],
        aggregatePredictions['state9']['confidence']
    )

    try:
        cursor.execute(query, values)
        db.commit()
    except:
        print('Error occurred while inserting data to session_data')
        return json.dumps({'success': False})

    db.close()
    return {
        'predictions': aggregatePredictions,
        'id': fetchLastToolId(),
        'success': True
    }


def insertCreatedTask(data):
    db = connect()
    cursor = db.cursor()

    query = """INSERT INTO CREATED_TASKS (SESSION_ID, TITLE, DESCRIPTION) VALUES (%s, %s, %s)"""

    values = (
        data['sessionId'],
        data['title'],
        data['description']
    )

    try:
        cursor.execute(query, values)
        db.commit()
    except:
        print('Error occurred while inserting data to created_tasks')
        return json.dumps({'success': False})

    db.close()
    return json.dumps({'success': True}, indent=4)


def insertEvaluationData(data):
    db = connect()
    cursor = db.cursor()

    query = """INSERT INTO EVALUATION_DATA (
                SESSION_ID,
                EXPERIENCE,
                PLATFORMS,
                MOST_USED_PLATFORM,
                MOST_TASKS,
                Q1,
                Q2,
                Q3,
                Q4,
                Q5,
                Q6,
                Q7,
                Q8,
                Q9,
                Q10,
                Q11,
                DIMENSIONS,
                COMMENT)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    values = (
        data['sessionId'],
        data['experience'],
        data['platforms'],
        data['most_used_platform'],
        data['most_tasks'],
        data['q1'],
        data['q2'],
        data['q3'],
        data['q4'],
        data['q5'],
        data['q6'],
        data['q7'],
        data['q8'],
        data['q9'],
        data['q10'],
        data['q11'],
        data['dimensions'],
        data['comment']
    )

    try:
        cursor.execute(query, values)
        db.commit()
    except:
        print('Error occurred while inserting data to evaluation_data')
        return json.dumps({'success': False})

    # Marking it finished
    query = """UPDATE SESSION_DATA SET FINISHED='Y' WHERE SESSION_ID=%s"""
    values = (data['sessionId'],)

    try:
        cursor.execute(query, values)
        db.commit()
    except:
        print('Error occurred updating FINISHED flag in session_data')
        return json.dumps({'success': False})

    db.close()
    return json.dumps({'success': True}, indent=4)
