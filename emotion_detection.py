import requests 
import json 

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text_to_analyze } }

    response = requests.post(url, headers=headers,json=input_json)   
    response_dict = response.json()
    result = response_dict.get('emotionPredictions')[0].get('emotionMentions')[0].get('span').get('text')
    return result
