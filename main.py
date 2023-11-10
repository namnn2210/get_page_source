from flask import Flask, request
from seleniumbase import Driver

import logging
import time
logging.basicConfig(filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
driver = Driver(uc=True, headless=False)


@app.route("/source", methods=['GET'])
def get_page_source():
    request_url = request.args.get('request_url')
    if request_url:
        driver.execute_script("window.open('"+request_url+"', '_blank')")
        time.sleep(10)
        page_source = driver.get_page_source()
        driver.close()
        return page_source
    return {'Error': 'Missing params'}


@app.route("/image", methods=['GET'])
def get_image():
    referer = request.args.get('referer')
    url = request.args.get('request_url')
    if referer is not None and url is not None:
        driver.execute_script("window.open('"+referer+"', '_blank')")
        time.sleep(15)
        driver.execute_script("window.open('"+url+"', '_blank')")
        time.sleep(10)
        for window_handle in (driver.window_handles)[1:]:
            driver.switch_to.window(window_handle)
            logging.info('Closing tab url: %s ' % driver.current_url)
            driver.close()
        driver.switch_to.window((driver.window_handles)[-1])
        return {'error_code': "200", 'description': 'Done', 'data': {'referer': referer, 'url': url}}
    return {'error_code': "406", 'description': 'Missing params', 'data': ''}


@app.route("/", methods=['GET'])
def index():
    return {'Error': 'Ok'}


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
