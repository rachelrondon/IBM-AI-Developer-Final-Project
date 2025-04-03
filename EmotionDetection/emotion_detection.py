import requests 
import json 

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text_to_analyze } }

    response = requests.post(url, headers=headers,json=input_json)   
    data = response.json()
    emotion_predictions = data['emotionPredictions']
    
    for prediction in emotion_predictions:
        score = prediction['emotion']

    joy_score = score['joy']
    anger_score = score['anger']
    disgust_score = score['disgust']
    fear_score = score['fear']
    sadness_score = score['sadness']
    dominant_emotion = max(score, key=score.get)

    if response.status_code == 400:
        return {
            'anger': None, 
            'disgust': None, 
            'fear': None, 
            'joy': None, 
            'sadness': None, 
            'dominant_emotion': None
        }
    else:
        return {
            'anger': anger_score,
            'disgust': disgust_score, 
            'fear': fear_score, 
            'joy': joy_score, 
            'sadness': sadness_score, 
            'dominant_emotion': dominant_emotion         
        }
