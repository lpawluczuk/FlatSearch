To transform file with path x into file with path x.out call:
"python __init__.py input_path.json"

To transform file into another file call:
"python __init__.py input_path.json output_path.json"

To transform file and send it into solr core call:
"python __init__.py input_path.json -w http://solr.address.com/solr/collection1/"
