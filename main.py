import os, sys, uuid
from flask import Flask, request, redirect, url_for, render_template, make_response, jsonify
import logging
from logging import FileHandler, Formatter
import tasks
import settings
import util
from zipfile import ZipFile

sys.path.append(settings.CALCULATION_PATH)
sys.path.append(settings.VISUALIZATION_PATH)

import create_newick_tree
import operonVisualUpdate

app = Flask(__name__)

# Utility functions, prior to start up.
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

def get_kegs():
    keg_files = util.returnRecursiveDirFiles(settings.KEG_FOLDER)
    keg_contents = {}
    keg_names = []
    for keg in keg_files:
        current_keg = open(keg, 'r')
        current_keg_genes = []
        for key in current_keg:
            new_org = key.replace('_', ' ').rstrip()
            current_keg_genes.append(new_org)
        keg_name = keg.split('/')[-1]
        keg_names.append(keg_name)
        keg_contents[keg_name] = current_keg_genes
    return keg_names, keg_contents


# Create Org, Operon, and Keg lists
ORGANISMS = get_organisms()
OPERONS = get_operons()
KEGS, KEG_DICT = get_kegs()

# Create the logger
file_handler = FileHandler(settings.LOG_FILE)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
app.logger.addHandler(file_handler)
app.debug = True

# Gets the splash page.
@app.route('/')
def get_main():
    return render_template('index.html')

# Handles POST and GET requests for Regular Queries
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
            return render_template("500.html"), 500

    return render_template('query.html', organisms=ORGANISMS, operons=OPERONS)

# Handles POST and GET requests for Keg Queries.
@app.route('/keg-query', methods=['GET', 'POST'])
def run_keg_query():
    if request.method == 'POST':
        try:
            request_id = uuid.uuid1()
            app.logger.info('Received task {0}'.format(str(request_id)))
            app.logger.info('Form: {0}'.format(str(request.form)))
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
            return render_template("500.html"), 500


    return render_template('keg-query.html', kegs=KEGS, operons=OPERONS)

# Get Keg data for a given Keg id.
@app.route('/keg/<keg>')
def get_keg_contents(keg):
    if keg in KEG_DICT:
        return jsonify(results=KEG_DICT[keg])
    else:
        return make_response('No keg named {0}'.format(keg), 404)

# Open the results page for a given request id
@app.route('/results/<requestid>')
def get_results(requestid, task_id=None):
    operon_names = util.get_operon_names(requestid)

    return render_template('results.html', operons=operon_names, request_id=requestid, task_id=task_id)

# Get a query image given a job, operon, and event
@app.route("/img/<requestid>/<operon>/<event>")
def get_image(requestid, operon, event):
    fullpath = settings.QUERY_STRING.format(requestid, operon, event)
    resp = make_response(open(fullpath).read())
    resp.content_type = 'image/png'
    return resp

# Utility calls
# Get static CSS files
@app.route("/static/css/<filename>")
def get_css(filename):
    fullpath = settings.TEMPLATE_STRING.format('css/' + filename)
    resp = make_response(open(fullpath).read())
    resp.content_type = 'text/css'
    return resp

# Get static image files that are not query images.
@app.route("/static/img/<filename>")
def get_wheel(filename):
    fullpath = settings.TEMPLATE_STRING.format('img/' + filename)
    resp = make_response(open(fullpath).read())
    resp.content_type = 'image/gif'
    return resp

# Get static JS files
@app.route("/static/js/<filename>")
def get_js(filename):
    fullpath = settings.TEMPLATE_STRING.format('js/' + filename)
    resp = make_response(open(fullpath).read())
    resp.content_type = 'text/javascript'
    return resp

# Check if a job is done or not.
@app.route("/job/<requestid>")
def check_job(requestid):
    path_to_job = os.path.join(settings.QUERY_FOLDER, requestid)
    try:
        task = tasks.createJob.AsyncResult(requestid)
        if task.ready():
            return make_response('OK', 200)
        else:
            task_status = open(os.path.join(path_to_job, 'status'), 'r')
            status = task_status.readline()
            if status == 'COMPLETE':
                return make_response('OK', 200)
            else:
                return make_response('ERROR', 500)

    except IOError:
        return make_response('NO', 404)


# Download a Zip archive of a given query and operon
@app.route("/download/<requestid>/<operon>")
def download_query_operon(requestid, operon):
    results_dir = os.path.join(settings.QUERY_FOLDER, '{0}/output_{0}/tree-gd-heat-diagrams_{0}'.format(requestid))
    new_archive_name = '{1}-{0}.zip'.format(requestid, operon)
    os.chdir(results_dir)
    new_archive = ZipFile(new_archive_name, 'w')
    for result in util.returnRecursiveDirFiles(results_dir):
        if '.zip' not in result.split('/')[-1]:
            new_archive.write(result.split('/')[-1])
    new_archive.close()
    os.chdir(settings.APPLICATION_PATH)

    resp = make_response(open(os.path.join(results_dir, new_archive_name)).read())
    resp.content_type = 'application/zip'
    resp.headers["Content-Disposition"] = "attachment; filename={0}.zip".format(new_archive_name)
    return resp

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def int_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run('0.0.0.0')
