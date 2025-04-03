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
    if not text_to_analyze:
        return jsonify({"message": "Invalid text! Please try again"}), 400
    # Call the perform_emotion_detection function
    emotions = perform_emotion_detection(text_to_analyze)

    # Convert values in the emotion dictionary to float
    def convert_value(value):
        try:
            return float(value)
        except ValueError:
            return 0

    emotions = {key: convert_value(value) for key, value in emotions.items()}

    # Determine the dominant emotion
    dominant_emotion = max(emotions, key=emotions.get, default=None)
    emotions["dominant_emotion"] = dominant_emotion

    if not text_to_analyze:
        return jsonify({
            "Invalid text! Please try again"
        })
    else:
        return jsonify({
            'For the given statement, the system response is': emotions,
            'The dominant emotion is': dominant_emotion
        })    

def perform_emotion_detection(text):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text} }

    response = requests.post(url, headers=headers, json=input_json)
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

if __name__ == '__main__':
    app.run(debug=True)