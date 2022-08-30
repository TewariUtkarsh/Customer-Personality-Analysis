from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
from customer.pipeline.pipeline import Pipeline
from customer.exception import CustomerException
from customer.logger import logging
import os, sys


app= Flask(__name__)

@app.route('/', methods=['POST','GET'])
@cross_origin()
def index():
    try:
        logging.info("Running Pipeline")
        raise Exception('test')
        p= Pipeline()
        res=p.run_pipeline()
        print(res)
        logging.info("Pipeline ran successfully")
        return f"Test Run Successfull [500]"
    except Exception as e:
        raise CustomerException(e, sys) from e

if __name__=='__main__':
    app.run(debug=True)