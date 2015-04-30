#!/usr/bin/python
'''
    GBEER Update Script

    Writen by: Jake Gregg, Miami University 2015

    Literally just run the script. It does everything. This is mostly a CRON job,
    but it can be executed if needed manually.
'''

import os, sys, site
import datetime, shutil

# Add the site packages to our path, as well as activating our virtual environment
site.addsitedir('/home/greggjs/.virtualenvs/flask/local/lib/python2.7/site-packages')
activate_this = os.path.expanduser('/home/greggjs/.virtualenvs/flask/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

# after activating the virtualenv, we can import whatever we need
import settings, util
from Bio import SeqIO,SeqFeature
from Bio.SeqRecord import SeqRecord

our_organisms = util.returnRecursiveDirs(settings.GENOME_INFOLDER)

def get_new_organisms(tarobject):
    count = 0
    for tarinfo in tarobject:
        count += 1
        if count % 500 == 0:
            sys.stdout.write(str(count) + ' records processed...\n')
        if tarinfo.name.split('/')[1] in our_organisms:
            yield tarinfo

month_dict = { 'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6, 'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}

# PARAMS for our command
temp_folder = os.path.join(settings.CALCULATION_PATH, 'temp_genomes')
genome_tar = '/genomes/Bacteria/all.gbk.tar.gz'

# Get the tarfile if we don't already have one. Saves time for testing.
if not os.path.exists(os.path.join(settings.CALCULATION_PATH, 'all.gbk.tar.gz')):
    sys.stdout.write("Retrieving archive from NCBI...\n")
    sys.stdout.flush()

    # make the temp folder, set permissions
    os.mkdir(temp_folder)
    os.chmod(temp_folder, settings.PEM_BITS)

    # Get the tar from the Gov't. Takes like 3 mins
    cmd = "ncftpget ftp.ncbi.nlm.nih.gov {0} {1}".format(settings.CALCULATION_PATH, genome_tar)
    os.system(cmd)

# Extract the contents of the tar archive
if not os.path.exists(temp_folder):
    sys.stdout.write("Extracting contents...\n")
    sys.stdout.flush()
    import tarfile
    tar = tarfile.open(os.path.join(settings.CALCULATION_PATH, 'all.gbk.tar.gz'))
    tar.extractall(path=temp_folder, members=get_new_organisms(tar))
    tar.close()

# Get a list of all files in current and new genome dicts
our_org_files = util.returnRecursiveDirFiles(settings.GENOME_INFOLDER)
new_org_files = util.returnRecursiveDirFiles(temp_folder)

sys.stdout.write('Getting genome files that need updating...')
sys.stdout.flush()
orgs_need_update = []
# iterate over all genomes
for i, new_org_file in enumerate(new_org_files):
    sys.stdout.write('.')
    sys.stdout.flush()
    our_org_file = our_org_files[i]

    # Look at the current GenBank files (new and ours)
    our_seq_record = SeqIO.parse(open(our_org_file), "genbank").next()
    new_seq_record = SeqIO.parse(open(new_org_file), "genbank").next()

    # Get the date for each record update
    our_seq_date_record = our_seq_record.annotations['date'].split('-')
    our_seq_date = datetime.date(int(our_seq_date_record[2]), month_dict[our_seq_date_record[1]], int(our_seq_date_record[0]))
    new_seq_date_record = new_seq_record.annotations['date'].split('-')
    new_seq_date = datetime.date(int(new_seq_date_record[2]), month_dict[new_seq_date_record[1]], int(new_seq_date_record[0]))

    # add it to the update queue if it needs updated
    if new_seq_date > our_seq_date:
        sys.stdout.write('\n' + our_org_file.split('/')[1].replace('_', ' ') + ' needs updating\n')
        orgs_need_update.append((our_org_file, new_org_file))

sys.stdout.write('\n' + str(len(orgs_need_update)) + ' Organisms need to be updated\n')
sys.stdout.flush()

# don't run the update scripts if there is nothing to update.
if len(orgs_need_update) == 0:
    sys.stdout.write("Files are up to date.\n")
    sys.stdout.flush()
else:
    for our_file, new_file in orgs_need_update:
        shutil.copy2(new_file, our_file)
    os.system('python {0}'.format(os.path.join(settings.CALCULATION_PATH, 'gbeer_developmental_pipeline.py')))

shutil.rmtree(temp_folder)
os.remove(os.path.join(settings.CALCULATION_PATH, 'all.gbk.tar.gz'))
sys.exit(0)

