import nltk
import re
import logging
import os.path
import sys
from flask                        import Flask, request, jsonify, render_template, flash
from flask_bootstrap              import Bootstrap
# from flask_sqlalchemy             import SQLAlchemy
from form_utilities.config        import Config
from form_utilities.forms         import RegisterForm
# from flask_json                   import FlaskJSON, JsonError, json_response, as_json
from nltk.sentiment.vader         import SentimentIntensityAnalyzer
from sklearn.linear_model         import LogisticRegression
from testing.swagger_ui           import blueprint_swagger
from utilities.model_file         import load_model_file
from utilities.text               import text_predict
from sklearn.pipeline             import Pipeline


HTTP_BAD_REQUEST = 400


# NLTK setting
nltk.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('punkt')


# Flask setting
app        = Flask(__name__)
bootstrap  = Bootstrap(app)
app.config.from_object(Config)


# Logging setting
logging.basicConfig(level  = logging.INFO,
                    format = "%(asctime)s  %(levelname)8s  %(filename)12s  %(funcName)12s  %(lineno)4d  %(message)s")
app_logger = logging.getLogger("app_logger")


# Register blueprint_swagger in app
app.register_blueprint(blueprint_swagger)


# Load model

#filename = "sentiment_model_pickle"               # Logistic Regression model
filename = "sentiment_model_pickle_default_sia"   # Sentiment Intensity Analysis model

if os.path.exists(str(filename)):
    model_files = load_model_file(filename, app_logger)
    # extract model from model file
    model       = model_files['model']
    app_logger.info('loaded_model:             ' + str(model))
else:
    sys.exit("NO sentiment_model_pickle file found in project folder.")


# cURL API endpoint
@app.route('/curl', methods = ['GET', 'POST'])
# to handle requests sent to this endpoint
def curl_scoring():
    '''
    curl --header "Content-Type: application/json"    \
         --request POST                               \
         --data '{"sentence":"xxx"}'                  \
         http://localhost:99/curl
    '''

    """
    This is the sentiment analysis API
    Call this api passing a sentence and get back its sentiment
    ---
    tags:
      - Sentiment Analysis API
    parameters:
      - name:        sentence
        type:        string
        required:    true
        description: The sentence for sentiment analysis
    responses:
      400:
        description: Bad Request
      200:
        description: Sentiments with their scores
        schema:
          score:     JSON
          properties:
            pos:
              type: float
              description: The positive sentiment
            neg:
              type: float
              description: The negative sentiment
            neu:
              type: float
              description: The neutral sentiment
            compound:
              type: float
              description: The compound sentiment                            
    """
    # to retrieve the input sentence related to this request
    # Flask helps to raise error if curl --data is not in JSON data type
    dict_request = request.get_json()
    app_logger.info('dict_request:      ' + str(dict_request))
    app_logger.info('dict_request type: ' + str(type(dict_request)))


    # raise error if failed to decode JSON object
    if len(dict_request) == 0:
        message  = "Failed to decode JSON object: No key/value pair in JSON. " \
                   "Expecting one, with key of 'sentence'."
        response = respond_with(message)
        return response
    elif len(dict_request) > 1:
        message  = "Failed to decode JSON object: More than one key/value pair in JSON. " \
                   "Expecting only one, with key of 'sentence'."
        response = respond_with(message)
        return response
    elif len(dict_request) == 1:
        # get_json() is modified to accept different values for one key.
        # In such case, it will return a list of values for the key.
        #   eg. {'sentence': ['I love you.', 'I hate you.']}
        # By default, it will only return the last value for the key.
        #   eg. {'sentence': 'I hate you.'}

        value = dict_request[next(iter(dict_request))]  # the value of the only key (either a str or a list)

        # more than one value for the key
        if type(value) is list:
            app_logger.info('dict_request:      ' + str(dict_request))
            app_logger.info('value:             ' + str(dict_request[next(iter(dict_request))]))
            app_logger.info('type(value):       ' + str(type(dict_request[next(iter(dict_request))])))

            if len(set(value)) == 1:
                # all the values are the same
                message = "Failed to decode JSON object: Repeated key/value pairs in JSON. " \
                          "Expecting only one, with key of 'sentence'."
                response = respond_with(message)
            else:
                message = "Failed to decode JSON object: More than one value for one key in JSON. " \
                          "Expecting only one, with key of 'sentence'."
                response = respond_with(message)
            return response
        elif "sentence" not in dict_request.keys():
            message  = "Failed to decode JSON object: Expecting key/value pair with key of 'sentence'."
            response = respond_with(message)
            return response
        elif not isinstance(dict_request["sentence"], str):
            message  = "Failed to decode JSON object: Expecting str data type for value in key/value pair " \
                       "(enclosed in double quotes)."
            response = respond_with(message)
            return response
    else:
        pass

    # extract the input data
    sentence = dict_request["sentence"]

    # raise error if the input sentence is not valid
    if len(re.findall("[a-zA-Z]", sentence)) == 0:
        message  = "Failed to find English letter in the input sentence. Please try again."
        response = respond_with(message)
        return response
    else:
        pass

    # Text pre-processing & Prediction
    dict_score = text_predict(sentence, model)

    # create and send a JSON response to the API caller
    return jsonify(score = dict_score, status = "complete", sentence = sentence)



# UI API endpoint
@app.route('/', methods = ['GET', 'POST'])
def index():
    """
    to return floats for sentiment strength based on the input sentence
    """
    title = "Sentiment Analysis"
    form  = RegisterForm()

    # When pressing the "analyse" button
    if form.validate_on_submit():

        sentence = request.form.get('sentence')

        # Text pre-processing & Prediction
        dict_score = text_predict(sentence, model)

        # Format output result
        if type(model) is SentimentIntensityAnalyzer:
            str_prediction = "Positive: " + str(dict_score["pos"]) + "  |  " + \
                             "Negative: " + str(dict_score["neg"]) + "  |  " + \
                             "Neutral: "  + str(dict_score["neu"]) + "  |  " + \
                             "Compound: " + str(dict_score["compound"])      
                             #+ \
                             #"  (Sentiment Intensity Analyzer)"

        elif type(model) is Pipeline and type(model['clf']) is LogisticRegression:
            str_prediction = "Score: " + str(dict_score['score']) + \
                             " (Logistic Regressor)"

        flash(str_prediction, category = "success")

    return render_template('index.html', title = title, form = form)


# Helper Methods
def respond_with(message):
    response = jsonify(status        = "error",
                       status_code   = str(HTTP_BAD_REQUEST) + " - Bad Request",
                       error_message = message)
    # set the status code to 400
    response.status_code = HTTP_BAD_REQUEST
    return response


if __name__ == '__main__':
    app.run(debug = True, port = 99, host ='0.0.0.0')
    # using host: can access from other PC, otherwise local host
