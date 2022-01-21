import json
import os
import logging
import time

from flask import Flask, request, jsonify, url_for
from flask_cors import CORS

from src.endpoint_utils import ERROR, OK
from src.logging_handler import init_logger, logger


########################################
# INIT Config
########################################
from src.main_pilotmanual import main, PATH

init_logger(log_level=logging.INFO)
app = Flask(__name__)
CORS(app)

log = logging.getLogger('werkzeug')
log.disabled = True

#########################################
# Main task
#########################################
def execute_task(json_data):
    return main(json_data)


#########################################
# Endpoint
#########################################
@app.route('/predict', methods=['POST'])
def check_match():
    logger.info("--- Request received ---")
    tstamp = str(time.time()).replace(".", "")
    os.mkdir(os.path.join(PATH, "assets", "tests", tstamp))

    json_data = request.json
    logger.info("Data loaded")
    
    if not json_data:
        logger.debug("Error: No JSON received")
        return json.dumps({'error': f'("Error: No JSON received")'}), 500
    
    try:
        result = execute_task(json_data)

        with open(os.path.join(PATH, "assets", "tests", tstamp, f"{tstamp}.txt"), "w") as f:
            json.dump(result, f)

        logger.info(result)

        return json.dumps(
            result
        )
    except Exception as ex:
        logger.exception("Exception while processing request")
        return json.dumps({'error': f'("{ex}")'})


    
@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({'status': 200})
    
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False, port=8893)