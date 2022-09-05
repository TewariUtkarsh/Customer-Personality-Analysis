from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
from customer.pipeline.pipeline import Pipeline
from customer.exception import CustomerException
from customer.logger import logging
from customer.config.configuration import Configuration
import os, sys


app= Flask(__name__)

@app.route('/', methods=['POST','GET'])
@cross_origin()
def index():
    try:
        # logging.info("Running Pipeline")
        # # raise Exception('test')
        # p= Pipeline()
        # res=p.run_pipeline()
        # print(res)
        # logging.info("Pipeline ran successfully")
        # return f"Test Run Successfull [500]"
        c= Configuration()
        print(c.get_data_validation_config())
    except Exception as e:
        raise CustomerException(e, sys) from e

if __name__=='__main__':
    # app.run(debug=True)
    # c= Configuration()
    # print(c.get_data_validation_config())
    p= Pipeline()

    print(p.run_pipeline())