import re
import logging

from flask                import request, jsonify, Blueprint
from flask_restplus       import Api, Resource, fields
from nltk.sentiment.vader import SentimentIntensityAnalyzer

HTTP_BAD_REQUEST = 400

# Logging setting
logging.basicConfig(level  = logging.INFO,
                    format = "%(asctime)s  %(levelname)8s  %(filename)12s  %(funcName)12s  %(lineno)4d  %(message)s")
logger = logging.getLogger("mylogger")

# NLTK setting
sid = SentimentIntensityAnalyzer()

# Flask Blueprint setting
# (Registration is in app.py)

# * Create Blueprint object
# (a collection of routes and other app-related functions
# that can be registered on a real application later)
# @paras:
#   name          The name of the blueprint. Will be prepended to each endpoint name.
#   import_name   The name of the blueprint package, usually __name__.
#                 This helps locate the root_path for the blueprint.
#   url_prefix    A path to prepend to all of the blueprint’s URLs,
#                 to make them distinct from the rest of the app’s routes.
blueprint_swagger = Blueprint('api_swagger',
                              __name__,
                              url_prefix = '/swagger-ui')

# * Create the main entry point for the app
# @paras:
#   app           The Flask application object or a Blueprint
#   version       The API version used in Swagger documentation
#   title         The API title used in Swagger documentation
#   description   The API description used in Swagger documentation
api_swagger       = Api(app         = blueprint_swagger,
                        version     = "1.0",
                        title       = "Sentiment Analyser",
                        description = "Score Sentiment for Sentence.")

# Group resources together
# whenever APIs are defined under a given namespace, they appear under a given heading in Swagger
# @paras:
#   name           The namespace name
#   description    A description for the space
#   path           An optional prefix path. If not provided, prefix is /+name
# In this example, the URL for the namespace is http://0.0.0.0:99/main
# which has the description as Main APIs in Swagger
name_space = api_swagger.namespace("Analyser APIs")
                                   # description = "A demonstration of Flask RestPlus APIs"

# Define models
# A thin wrapper on fields dict to store API doc metadata.
# Can also be used for response marshalling.
# Here, use 'model' to receive/send info in JSON format.
# @paras:
#   name           The model public name
# The API which will use this model will expect JSON with a key as "sentence".
model = api_swagger.model("Sentence Model",
                          {'sentence': fields.String(required   = True,
                                                     decription = "Sentence for sentiment analysis",
                                                     help       = "Sentence cannot be blank.")})

# Define endpoints under the route "/" inside the class
# the APIs can be accessed at the path http://127.0.0.1:5000/
'''
in project dir, run:
$ FLASK_APP=app.py flask run
'''
# route definition at http://127.0.0.1:5000/main/
# It expects a sentence to be sent as a String.
@name_space.route("/")
#@name_space.route("/<int:id>")
class MainClass(Resource):
    # define docs for the API in Swagger
    # @paras
    #   response   defines the possible HTTP status codes and their description
    #   params     defines the expected parameter, in this case, "sentence", and a help text

    @api_swagger.doc(responses = {200: "OK",
                                  400: "Bad Request",
                                  500: "Internal Server Error"})


    # define the model request API expects
    @api_swagger.expect(model)
    def post(self):

        # to retrieve the input sentence related to this request
        # Flask helps to raise error if curl --data is not in JSON data type
        dict_request = request.json
        logger.info('dict_request:      ' + str(dict_request))
        logger.info('dict_request type: ' + str(type(dict_request)))

        # raise error if failed to decode JSON object
        if len(dict_request) == 0:
            message = "Failed to decode JSON object: No key/value pair in JSON. " \
                      "Expecting one, with key of 'sentence'."
            response = respond_with(message)
            return response
        elif len(dict_request) > 1:
            message = "Failed to decode JSON object: More than one key/value pair in JSON. " \
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
                message = "Failed to decode JSON object: Expecting key/value pair with key of 'sentence'."
                response = respond_with(message)
                return response
            elif not isinstance(dict_request["sentence"], str):
                message = "Failed to decode JSON object: Expecting str data type for value in key/value pair " \
                          "(enclosed in double quotes)."
                response = respond_with(message)
                return response
        else:
            pass

        # extract the input data
        sentence = dict_request["sentence"]

        # raise error if the input sentence is not valid
        if len(re.findall("[a-zA-Z]", sentence)) == 0:
            message = "Failed to find English letter in the input sentence. Please try again."
            response = respond_with(message)
            return response
        else:
            pass

        # return floats for sentiment strength based on the input sentence
        try:
            dict_score = sid.polarity_scores(sentence)
        except:
            print("error in sid.polarity_scores(sentence)")

        return {
                    "status":   "Sentence analysed",
                    "sentence": request.json["sentence"],
                    "result":   dict_score
               }

# Helper Methods
def respond_with(message):
    response = jsonify(status        = "error",
                       status_code   = str(HTTP_BAD_REQUEST) + " - Bad Request",
                       error_message = message)
    # set the status code to 400
    response.status_code = HTTP_BAD_REQUEST
    return response
