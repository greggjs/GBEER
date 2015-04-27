import stat

APPLICATION_PATH = '/vagrant/GBEER/'
LOG_FILE = os.path.join(APPLICATION_PATH, 'logs/gbeer.log')

QUERY_FOLDER = os.path.join(APPLICATION_PATH, 'queries/')

CALCULATION_PATH = os.path.join(APPLICATION_PATH, 'gene_block_evolution')
VISUALIZATION_PATH = os.path.join(APPLICATION_PATH, operonVisualization')

OPERON_DICT = os.path.join(CALCULATION_PATH, 'regulonDB/operon_names_and_genes.txt')
OPERON_INFOLDER = os.path.join(CALCULATION_PATH, 'optimized_operon/')
GENOME_INFOLDER = os.path.join(CALCULATION_PATH, 'genomes/')
MAPPING_CSV = os.path.join(VISUALIZATION_PATH, 'data/mapping.csv')

TEMPLATE_STRING = os.path.join(APPLICATION_PATH, 'templates/{0}')
QUERY_STRING = os.path.join(QUERY_FOLDER, '{0}/output_{0}/tree-gd-heat-diagrams_{0}/{1}_{2}')
PEM_BITS = stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH
