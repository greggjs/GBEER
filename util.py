import settings
import uuid
import os, sys
import shutil
from flask import request

def returnRecursiveDirs(root_dir):
    return [name for name in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, name))]

def returnRecursiveDirFiles(root_dir):
    result = []
    for path, dir_name, flist in os.walk(root_dir):
        for f in flist:
            fname = os.path.join(path, f)
            if os.path.isfile(fname):
                result.append(fname)
    return result

def make_genome_dir(request_id, form_data):
    os.mkdir(os.path.join(settings.QUERY_FOLDER, '{0}/genomes'.format(str(request_id))))
    os.chmod(os.path.join(settings.QUERY_FOLDER, '{0}/genomes'.format(str(request_id))), settings.PEM_BITS)
    for key, value in form_data.iteritems():
        if 'orgList' in key and value is not unicode(''):
            genome_dir = form_data.get(key).replace(' ', '_')
            os.mkdir(os.path.join(settings.QUERY_FOLDER, '{0}/genomes/{1}'.format(str(request_id), genome_dir)))
            os.chmod(os.path.join(settings.QUERY_FOLDER, '{0}/genomes/{1}'.format(str(request_id), genome_dir)), settings.PEM_BITS)
            for f in os.listdir(os.path.join(settings.GENOME_INFOLDER, genome_dir)):
                shutil.copy2(os.path.join(settings.GENOME_INFOLDER, genome_dir, f), os.path.join(settings.QUERY_FOLDER, '{0}/genomes/{1}/{2}'.format(str(request_id), genome_dir, f)))

def make_query_file(request_id, form_data):
    files = returnRecursiveDirFiles(os.path.join(settings.QUERY_FOLDER, '{0}/genomes/'.format(str(request_id))))
    query_file = open(os.path.join(settings.QUERY_FOLDER, '{0}/phylo_tree.txt'.format(str(request_id))), 'w')
    os.chmod(os.path.join(settings.QUERY_FOLDER, '{0}/phylo_tree.txt'.format(str(request_id))), settings.PEM_BITS)
    for f in files:
        gene = f.split('/')[-1].rstrip('.gbk')
        query_file.write(gene + '\n')

def make_operon_filter(request_id, form_data):
    filter_file = open(os.path.join(settings.QUERY_FOLDER, '{0}/filter_file'.format(str(request_id))), 'w')
    os.chmod(os.path.join(settings.QUERY_FOLDER, '{0}/filter_file'.format(str(request_id))), settings.PEM_BITS)
    operon_list = []
    for key, value in form_data.iteritems():
        if 'opList' in key and value is not unicode(''):
            filter_file.write(value + '\n')
            operon_list.append(value)
    return operon_list

def get_operon_names(request_id):
    filter_file = open(os.path.join(settings.QUERY_FOLDER, '{0}/filter_file'.format(str(request_id))), 'r')
    operon_list = []
    for line in filter_file:
        operon_list.append(line.rstrip())
    return operon_list

def make_operon_dir(request_id, form_data):
    os.mkdir(os.path.join(settings.QUERY_FOLDER, '{0}/operons'.format(str(request_id))))
    os.chmod(os.path.join(settings.QUERY_FOLDER, '{0}/operons'.format(str(request_id))), settings.PEM_BITS)
    files = returnRecursiveDirFiles(settings.OPERON_INFOLDER)
    for f in files:
        for key, value in form_data.iteritems():
            if 'opList' in key and value in f:
                shutil.copy2(f, os.path.join(settings.QUERY_FOLDER, '{0}/operons'.format(str(request_id))))
