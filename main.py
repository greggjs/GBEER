import os, sys, uuid, csv, subprocess, shutil
from flask import Flask, request, redirect, url_for, render_template, make_response
import tasks
import settings
import util

sys.path.append(settings.CALCULATION_PATH)
sys.path.append(settings.VISUALIZATION_PATH)

import create_newick_tree
import operonVisualUpdate

app = Flask(__name__)

def get_operons():
    operon_file = open(settings.OPERON_DICT, 'r')
    operons = ['']
    for operon in operon_file:
        operons.append(operon.split('\t')[0])
    return operons

def get_organisms():
    org_dir = util.returnRecursiveDirs(settings.GENOME_INFOLDER)
    org_list = ['']
    for org in org_dir:
        split_line = org.split('/')
        new_org = '{0}'.format(split_line[-1].replace('_', ' '))
        org_list.append(new_org)
    return org_list

# Create Org & Operon lists
ORGANISMS = get_organisms()
OPERONS = get_operons()

# Create the logger
import logging
from logging import FileHandler, Formatter
file_handler = FileHandler(settings.LOG_FILE)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
app.logger.addHandler(file_handler)
app.debug = True

@app.route('/')
def get_main():
    return render_template('index.html')

@app.route('/query', methods=['GET', 'POST'])
def run_query():
    if request.method == 'POST':
        try:
            request_id = uuid.uuid1()
            app.logger.info('Received task {0}'.format(str(request_id)))
            # Make a dir for the request
            os.mkdir(os.path.join(settings.APPLICATION_PATH, 'queries', str(request_id)))
            os.chmod(os.path.join(settings.APPLICATION_PATH, 'queries', str(request_id)), settings.PEM_BITS)
            # Preprocess request for functions
            util.make_genome_dir(request_id, request.form)
            util.make_query_file(request_id, request.form)
            operon_names = util.make_operon_filter(request_id, request.form)
            util.make_operon_dir(request_id, request.form)

            current_task = tasks.createJob.apply_async([request_id], task_id=str(request_id))
            app.logger.info('Created task {0} running on Celery Queue'.format(str(request_id)))
            return redirect('results/{0}'.format(request_id))
        except Exception as e:
            app.logger.error('Error creating task {0}'.format(str(request_id)))
            app.logger.error(str(e))

    return render_template('query.html', organisms=ORGANISMS, operons=OPERONS)

@app.route('/results/<requestid>')
def get_results(requestid, task_id=None):
    operon_names = util.get_operon_names(requestid)

    return render_template('results.html', operons=operon_names, request_id=requestid, task_id=task_id)

@app.route("/img/<requestid>/<operon>/<event>")
def get_image(requestid, operon, event):
    fullpath = settings.QUERY_STRING.format(requestid, operon, event)
    resp = make_response(open(fullpath).read())
    resp.content_type = 'image/png'
    return resp

@app.route("/static/css/<filename>")
def get_css(filename):
    fullpath = settings.TEMPLATE_STRING.format('css/' + filename)
    resp = make_response(open(fullpath).read())
    resp.content_type = 'text/css'
    return resp

@app.route("/static/img/<filename>")
def get_wheel(filename):
    fullpath = settings.TEMPLATE_STRING.format('img/' + filename)
    resp = make_response(open(fullpath).read())
    resp.content_type = 'image/gif'
    return resp

@app.route("/static/js/<filename>")
def get_js(filename):
    fullpath = settings.TEMPLATE_STRING.format('js/' + filename)
    resp = make_response(open(fullpath).read())
    resp.content_type = 'text/javascript'
    return resp

@app.route("/job/<requestid>")
def check_job(requestid):
    task = tasks.createJob.AsyncResult(requestid)
    if task.ready():
        return make_response('OK', 200)
    else:
        return make_response('NO', 404)

if __name__ == '__main__':
    app.run('0.0.0.0')
