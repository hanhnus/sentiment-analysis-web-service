'''
Run test case in PyCharm Terminal:
$ pytest -vv --disable-warnings
--v: to show the result for every test case
'''

import json
from app                    import app, logger
from pathlib                import Path
# import JSONMixin to handle the 1-key multi-value scenario
from werkzeug.wrappers.json import JSONMixin
from json.decoder           import JSONDecodeError

DATA_DIR = Path(__file__).parents[0]

# empty payload
def test_01():
    payload              = '{}'
    expected_status_code = 400
    expected_response    = {
        "error_message": "Failed to decode JSON object: No key/value pair in JSON. "
                         "Expecting one, with key of 'sentence'.",
        "status":        "error",
        "status_code":   "400 - Bad Request"
    }

    with app.test_client() as client:
        # send request to server, and get response
        response = client.post('http://localhost:98/curl',
                               json = JSONMixin().json_module.loads(payload,
                                                                    object_pairs_hook = my_obj_pairs_hook))
        # check whether we get the expected response back
        assert response.status_code      == expected_status_code
        assert json.loads(response.data) == expected_response

# more than one element in payload
# test_02 same key, same value
# test_03 same key, diff value
# test_04 diff key, same value
# test_05 diff key, diff value

# same key, same value
def test_02():
    payload              = '{"sentence": "I feel good.", ' \
                           ' "sentence": "I feel good."} '
    expected_status_code = 400
    expected_response    = {
        "error_message": "Failed to decode JSON object: Repeated key/value pairs in JSON. " \
                         "Expecting only one, with key of 'sentence'.",
        "status":        "error",
        "status_code":   "400 - Bad Request"
    }

    with app.test_client() as client:
        # send request to server, and get response
        response = client.post('http://localhost:98/curl',
                               json = JSONMixin().json_module.loads(payload,
                                                                    object_pairs_hook = my_obj_pairs_hook))
        # check whether we get the expected response back
        assert response.status_code      == expected_status_code
        assert json.loads(response.data) == expected_response

# same key, diff value
def test_03():
    payload              = '{"sentence": "I feel good.", ' \
                           ' "sentence": "I feel bad.",  ' \
                           ' "sentence": "I feel great."}'
    expected_status_code = 400
    expected_response    = {
        "error_message": "Failed to decode JSON object: More than one value for one key in JSON. " \
                         "Expecting only one, with key of 'sentence'.",
        "status":        "error",
        "status_code":   "400 - Bad Request"
    }

    with app.test_client() as client:
        # send request to server, and get response
        response = client.post('http://localhost:98/curl',
                               json = JSONMixin().json_module.loads(payload,
                                                                    object_pairs_hook = my_obj_pairs_hook))
        # check whether we get the expected response back
        assert response.status_code      == expected_status_code
        assert json.loads(response.data) == expected_response

# diff key, same value
def test_04():
    payload              = '{"sentence_1": "I feel good.", ' \
                           ' "sentence_2": "I feel good."} '
    expected_status_code = 400
    expected_response    = {
        "error_message": "Failed to decode JSON object: More than one key/value pair in JSON. " \
                         "Expecting only one, with key of 'sentence'.",
        "status":        "error",
        "status_code":   "400 - Bad Request"
    }

    with app.test_client() as client:
        # send request to server, and get response
        response = client.post('http://localhost:98/curl',
                               json = JSONMixin().json_module.loads(payload,
                                                                    object_pairs_hook = my_obj_pairs_hook))
        # check whether we get the expected response back
        assert response.status_code      == expected_status_code
        assert json.loads(response.data) == expected_response

# diff key, diff value
def test_05():
    payload              = '{"sentence_1": "I feel good.", ' \
                           ' "sentence_2": "I feel bad."}  '
    expected_status_code = 400
    expected_response    = {
        "error_message": "Failed to decode JSON object: More than one key/value pair in JSON. " \
                         "Expecting only one, with key of 'sentence'.",
        "status":        "error",
        "status_code":   "400 - Bad Request"
    }

    with app.test_client() as client:
        # send request to server, and get response
        response = client.post('http://localhost:98/curl',
                               json = JSONMixin().json_module.loads(payload,
                                                                    object_pairs_hook = my_obj_pairs_hook))
        # check whether we get the expected response back
        assert response.status_code      == expected_status_code
        assert json.loads(response.data) == expected_response

# variances on "diff key, diff value"
def test_06():
    payload              = '{"not_sentence": "I feel good.", ' \
                           ' "not_sentence": "I feel good."} '
    expected_status_code = 400
    expected_response    = {
        "error_message": "Failed to decode JSON object: Repeated key/value pairs in JSON. " \
                         "Expecting only one, with key of 'sentence'.",
        "status":        "error",
        "status_code":   "400 - Bad Request"
    }

    with app.test_client() as client:
        # send request to server, and get response
        response = client.post('http://localhost:98/curl',
                               json = JSONMixin().json_module.loads(payload,
                                                                    object_pairs_hook = my_obj_pairs_hook))
        # check whether we get the expected response back
        assert response.status_code      == expected_status_code
        assert json.loads(response.data) == expected_response

def test_07():
    payload              = '{"not_sentence": "I feel good.", ' \
                           ' "not_sentence": "I feel bad.",  ' \
                           ' "not_sentence": "I feel great."}'
    expected_status_code = 400
    expected_response    = {
        "error_message": "Failed to decode JSON object: More than one value for one key in JSON. " \
                         "Expecting only one, with key of 'sentence'.",
        "status":        "error",
        "status_code":   "400 - Bad Request"
    }

    with app.test_client() as client:
        # send request to server, and get response
        response = client.post('http://localhost:98/curl',
                               json = JSONMixin().json_module.loads(payload,
                                                                    object_pairs_hook = my_obj_pairs_hook))
        # check whether we get the expected response back
        assert response.status_code      == expected_status_code
        assert json.loads(response.data) == expected_response

def test_08():
    payload              = '{"sentence":     "I feel good.", ' \
                           ' "not_sentence": "I feel good."} '
    expected_status_code = 400
    expected_response    = {
        "error_message": "Failed to decode JSON object: More than one key/value pair in JSON. " \
                         "Expecting only one, with key of 'sentence'.",
        "status":        "error",
        "status_code":   "400 - Bad Request"
    }

    with app.test_client() as client:
        # send request to server, and get response
        response = client.post('http://localhost:98/curl',
                               json = JSONMixin().json_module.loads(payload,
                                                                    object_pairs_hook = my_obj_pairs_hook))
        # check whether we get the expected response back
        assert response.status_code      == expected_status_code
        assert json.loads(response.data) == expected_response

def test_09():
    payload              = '{"not_sentence": "I feel good.", ' \
                           ' "sentence":     "I feel good."} '
    expected_status_code = 400
    expected_response    = {
        "error_message": "Failed to decode JSON object: More than one key/value pair in JSON. " \
                         "Expecting only one, with key of 'sentence'.",
        "status":        "error",
        "status_code":   "400 - Bad Request"
    }

    with app.test_client() as client:
        # send request to server, and get response
        response = client.post('http://localhost:98/curl',
                               json = JSONMixin().json_module.loads(payload,
                                                                    object_pairs_hook = my_obj_pairs_hook))
        # check whether we get the expected response back
        assert response.status_code      == expected_status_code
        assert json.loads(response.data) == expected_response

def test_10():
    payload              = '{"sentence":     "I feel good.", ' \
                           ' "not_sentence": "I feel bad."}  '
    expected_status_code = 400
    expected_response    = {
        "error_message": "Failed to decode JSON object: More than one key/value pair in JSON. " \
                         "Expecting only one, with key of 'sentence'.",
        "status":        "error",
        "status_code":   "400 - Bad Request"
    }

    with app.test_client() as client:
        # send request to server, and get response
        response = client.post('http://localhost:98/curl',
                               json = JSONMixin().json_module.loads(payload,
                                                                    object_pairs_hook = my_obj_pairs_hook))
        # check whether we get the expected response back
        assert response.status_code      == expected_status_code
        assert json.loads(response.data) == expected_response

def test_11():
    payload              = '{"not_sentence": "I feel good.", ' \
                           ' "sentence":     "I feel bad."}  '
    expected_status_code = 400
    expected_response    = {
        "error_message": "Failed to decode JSON object: More than one key/value pair in JSON. " \
                         "Expecting only one, with key of 'sentence'.",
        "status":        "error",
        "status_code":   "400 - Bad Request"
    }

    with app.test_client() as client:
        # send request to server, and get response
        response = client.post('http://localhost:98/curl',
                               json = JSONMixin().json_module.loads(payload,
                                                                    object_pairs_hook = my_obj_pairs_hook))
        # check whether we get the expected response back
        assert response.status_code      == expected_status_code
        assert json.loads(response.data) == expected_response

# one element in payload
# key is not "sentence"
def test_12():
    payload              = '{"not_sentence": "I feel good."}'
    expected_status_code = 400
    expected_response    = {
        "error_message": "Failed to decode JSON object: Expecting key/value pair with key of 'sentence'.",
        "status":        "error",
        "status_code":   "400 - Bad Request"
    }

    with app.test_client() as client:
        # send request to server, and get response
        response = client.post('http://localhost:98/curl',
                               json = JSONMixin().json_module.loads(payload,
                                                                    object_pairs_hook = my_obj_pairs_hook))
        # check whether we get the expected response back
        assert response.status_code      == expected_status_code
        assert json.loads(response.data) == expected_response


# JSON Decode Error
# value is not string
def test_13():
    payload              = '{"sentence":value_not_string}'

    with app.test_client() as client:
        # send request to server, and get response
        try:
            response = client.post('http://localhost:98/curl',
                                   json = JSONMixin().json_module.loads(payload,
                                                                        object_pairs_hook = my_obj_pairs_hook))
        except JSONDecodeError as e:
            # check whether we get the expected response back
            assert e.args == ('Expecting value: line 1 column 13 (char 12)',)

# key is not string
def test_14():
    payload = '{sentence:"key_not_string"}'

    with app.test_client() as client:
        # send request to server, and get response
        try:
            response = client.post('http://localhost:98/curl',
                                   json=JSONMixin().json_module.loads(payload,
                                                                      object_pairs_hook=my_obj_pairs_hook))
        except JSONDecodeError as e:
            # check whether we get the expected response back
            assert e.args == ('Expecting property name enclosed in double quotes: line 1 column 2 (char 1)',)


# text pre-processing
def test_21():
    payload              = '{"sentence": "I\'D l@&$%%^ov*)e t+++o '    \
                           '<p>haVe<h1> thRee cUPs   of Lat81405878tè' \
                           '<br /><br />frOM yo74593ur caffè. "}'
    expected_status_code = 200
    expected_response    = {
       "score": {
         "compound": 0.6369,
         "neg":      0.0,
         "neu":      0.543,
         "pos":      0.457
       },
       "sentence": "id love three cups latte caffe",
       "status":   "complete"
     }

    with app.test_client() as client:
        # send request to server, and get response
        response = client.post('http://localhost:98/curl',
                               json = JSONMixin().json_module.loads(payload,
                                                                    object_pairs_hook = my_obj_pairs_hook))
        # check whether we get the expected response back
        assert response.status_code      == expected_status_code
        assert json.loads(response.data) == expected_response


# ML model tests
def test_101():
    payload              = '{"sentence": "I feel good."}'
    expected_status_code = 200
    expected_response    = {
       "score": {
         "compound": 0.4404,
         "neg":      0.0,
         "neu":      0.256,
         "pos":      0.744
       },
       "sentence": "feel good",
       "status":   "complete"
     }

    with app.test_client() as client:
        # send request to server, and get response
        response = client.post('http://localhost:98/curl',
                               json = JSONMixin().json_module.loads(payload,
                                                                    object_pairs_hook = my_obj_pairs_hook))
        # check whether we get the expected response back
        assert response.status_code      == expected_status_code
        assert json.loads(response.data) == expected_response

def test_102():
    payload              = '{"sentence": "I feel bad."}'
    expected_status_code = 200
    expected_response    = {
       "score": {
         "compound": -0.5423,
         "neg":       0.778,
         "neu":       0.222,
         "pos":       0.0
       },
       "sentence": "feel bad",
       "status":   "complete"
     }

    with app.test_client() as client:
        # send request to server, and get response
        response = client.post('http://localhost:98/curl',
                               json = JSONMixin().json_module.loads(payload,
                                                                    object_pairs_hook = my_obj_pairs_hook))
        # check whether we get the expected response back
        assert response.status_code      == expected_status_code
        assert json.loads(response.data) == expected_response








# test through .json file
# def api_test():
#     dataset_fname = DATA_DIR.joinpath('test_cases_auto.json')
#
#     # load all the test cases
#     with open(dataset_fname) as f:
#         test_cases = json.load(f)
#
#     for test_case in test_cases:
#         with app.test_client() as client:
#             payload              = test_case["payload"]
#             expected_status_code = test_case["expected_status_code"]
#             expected_response    = test_case["expected_response"]
#             # send request to server, and get response
#             response = client.post('http://localhost:98/curl',
#                                    json = payload)
#             # check whether we get the expected response back
#             assert response.status_code      == expected_status_code
#             assert json.loads(response.data) == expected_response





# helper function
# convert 1-key vs multi-value
#      to 1-key vs 1-list with multi-value
def my_obj_pairs_hook(lst):
    result = {}
    count  = {}
    for key, val in lst:
        if key in count:
            count[key] = 1 + count[key]
        else:
            count[key] = 1
        if key in result:
            if count[key] > 2:
                result[key].append(val)
            else:
                result[key] = [result[key], val]
        else:
            result[key] = val
    return result
