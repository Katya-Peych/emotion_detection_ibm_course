"""
Flask application for emotion detection.

This module provides a web interface for analyzing emotions in text
using the Watson NLP emotion detection service.
"""

from flask import Flask, render_template, request, jsonify
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route("/")
def home():
    """
    Render the home page.
    
    Returns:
        str: Rendered HTML template for the home page.
    """
    return render_template("index.html")

@app.route("/emotionDetector", methods=["GET", "POST"])
def emotion_detector_route():
    """
    Handle emotion detection requests via GET or POST methods.
    
    For GET requests, expects 'textToAnalyze' query parameter.
    For POST requests, expects JSON with 'text' field.
    
    Returns:
        JSON response containing either the emotion analysis results
        or an error message for invalid input.
    """
    if request.method == "GET":
        # Handle GET request with query parameters
        text_to_analyze = request.args.get("textToAnalyze")
        if not text_to_analyze or not text_to_analyze.strip():
            return jsonify({"response": "Invalid text! Please try again!"})
    else:
        # Handle POST request with JSON data
        data = request.get_json()
        if not data or "text" not in data or not data["text"] or not data["text"].strip():
            return jsonify({"response": "Invalid text! Please try again!"})
        text_to_analyze = data["text"]

    result = emotion_detector(text_to_analyze)
    
    # Check if dominant_emotion is None (indicating an error)
    if result['dominant_emotion'] is None:
        return jsonify({"response": "Invalid text! Please try again!"})

    formatted_response = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']}, "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )

    return jsonify({"response": formatted_response})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
