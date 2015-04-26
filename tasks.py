from celery import Celery
import settings
import sys, os, site

site.addsitedir('/home/greggjs/.virtualenvs/flask/local/lib/python2.7/site-packages')

activate_this = os.path.expanduser('/home/greggjs/.virtualenvs/flask/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

sys.path.append(settings.CALCULATION_PATH)
sys.path.append(settings.VISUALIZATION_PATH)

import create_newick_tree
import operonVisualUpdate

app = Celery('tasks', backend='amqp', broker='amqp://guest@localhost//')
app.conf.update(CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml'])

@app.task
def add(x, y):
    return x + y

@app.task
def createJob(request_id):
    # Create the phylo tree for request
    create_newick_tree.get_newick_tree(os.path.join(settings.QUERY_FOLDER, '{0}/genomes'.format(str(request_id))),
        os.path.join(settings.QUERY_FOLDER, '{0}/out_tree.nwk'.format(str(request_id))),
        os.path.join(settings.QUERY_FOLDER, '{0}/phylo_tree.txt'.format(str(request_id))), str(request_id))

    # Do operon comparisons on request
    event_cmd = 'python /vagrant/GBEER/gene_block_evolution/make_event_distance_matrix.py -i {0} -I {1} -o {2} -F {3}'.format(
        settings.OPERON_DICT, settings.OPERON_INFOLDER,
        os.path.join(settings.QUERY_FOLDER, '{0}'.format(str(request_id))),
        os.path.join(settings.QUERY_FOLDER, '{0}/filter_file'.format(str(request_id)))
    )
    os.system(event_cmd)

    # Normalize results of request
    matrix_cmd = 'python /vagrant/GBEER/gene_block_evolution/get_output_probs.py -i {0}'.format(
        os.path.join(settings.QUERY_FOLDER, '{0}/event_dict.p'.format(str(request_id)))
    )
    os.system(matrix_cmd)

    operonVisualUpdate.create_operon_images(
        settings.OPERON_INFOLDER,
        os.path.join(settings.QUERY_FOLDER, '{0}/asma_outlist.txt'.format(str(request_id))),
        os.path.join(settings.QUERY_FOLDER, '{0}/out_tree.nwk'.format(str(request_id))),
        os.path.join(settings.QUERY_FOLDER, '{0}/event_dict.p'.format(str(request_id))),
        os.path.join(settings.QUERY_FOLDER, '{0}/output'.format(str(request_id))),
        request_id
    )

    return True
