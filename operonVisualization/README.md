# operonVisualization

Evolution of gene blocks in proteobacteria can be described by a small set of events: insertions, deletions and duplications. The figures generated will help understand the evolutionary rate.

This program requires the following inputs:

1) Genome block information files.

2) A csv file mapping accession numbers to corresponding organism names.

3) A newick formatted phylogenetic tree.

4) An event pickled dictionary containing each operon's events and number of their observations.

5) An output directory of user's choice.

Note: Samples for each of the inputs are available in 'data' folder.

This command should run generate the required figures:

./operonVisual.py -n data/optimized_results_proteobacteria -m data/mapping.csv -t data/reorder.nwk -e data/event_dict.p -o [path to your choice of output directory]

Output:

1) CSV files with all the z-scores in each operon's event

2) Directory with genome diagrams alone. 

3) Directory with diagram containing tree, genome diragram and heat map for each operon event.
