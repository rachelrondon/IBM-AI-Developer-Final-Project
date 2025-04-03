from flask import Flask, request, jsonify, render_template
import requests 
import json 

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/emotionDetector', methods=['GET'])
def emotion_detector_route():
    text_to_analyze = request.args.get('textToAnalyze')
    print(f"Received text: {text_to_analyze}")

    if text_to_analyze:
          # Call the perform_emotion_detection function
        emotions = perform_emotion_detection(text_to_analyze)

        # Determine the dominant emotion
        dominant_emotion = max(emotions, key=emotions.get, default=None)
        emotions["dominant_emotion"] = dominant_emotion
        
        return jsonify({
            'For the given statement, the system response is': emotions,
            'The dominant emotion is': dominant_emotion
        })  
    else:
        print("No text provided, returning error response.")  # Debugging message
        return {
           "message": "Invalid text! Please provide text to analyze."
        }

def perform_emotion_detection(text):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text} }

    response = requests.post(url, headers=headers, json=input_json)

    if response.status_code != 200:
        return {
            'anger': 0, 
            'disgust': 0, 
            'fear': 0, 
            'joy': 0, 
            'sadness': 0
        }
    
    try: 
        data = response.json()
        emotion_predictions = data['emotionPredictions']
        score = emotion_predictions[0]['emotion']

        joy_score = score.get('joy', 0)
        anger_score = score.get('anger', 0)
        disgust_score = score.get('disgust', 0)
        fear_score = score.get('fear', 0)
        sadness_score = score.get('sadness', 0)

        return {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score
        }
    
    except (KeyError, IndexError, ValueError) as e:

        return {
            'anger': 0, 
            'disgust': 0, 
            'fear': 0, 
            'joy': 0, 
            'sadness': 0
        }

if __name__ == '__main__':
    app.run(debug=True)