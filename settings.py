import stat

APPLICATION_PATH = '/vagrant/GBEER/'
LOG_FILE = '/vagrant/GBEER/logs/gbeer.log'

QUERY_FOLDER = '/vagrant/GBEER/queries/'

CALCULATION_PATH = '/vagrant/GBEER/gene_block_evolution'
VISUALIZATION_PATH = '/vagrant/GBEER/operonVisualization'

OPERON_DICT = '/vagrant/GBEER/gene_block_evolution/regulonDB/operon_names_and_genes.txt'
OPERON_INFOLDER = '/vagrant/GBEER/gene_block_evolution/optimized_operon/'
GENOME_INFOLDER = '/vagrant/GBEER/gene_block_evolution/genomes/'
MAPPING_CSV = '/vagrant/GBEER/operonVisualization/data/mapping.csv'

TEMPLATE_STRING = '/vagrant/GBEER/templates/{0}'
QUERY_STRING = '/vagrant/GBEER/queries/{0}/output_{0}/tree-gd-heat-diagrams_{0}/{1}_{2}'
PEM_BITS = stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH
