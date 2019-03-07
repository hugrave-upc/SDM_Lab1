#!/bin/bash

## Main script to evolve the graph

# importing the utility library
. ../Utility/utility.sh

NEO4J_IMPORT="/var/lib/neo4j/import/"

add_comp_script="add_companies.cyph"
add_uni_script="add_universities.cyph"
add_rev_script="add_reviews.cyph"
add_aff_script="add_affiliations.cyph"
add_aff_python="addAffiliations.py"
add_indexes_script="add_indexes.cyph"
aff_csv="out_csv/affiliations.csv"

if [[ ! ( -f "$add_comp_script" || \
            -f "$add_uni_script" || \
            -f "$add_rev_script" || \
            -f "$add_aff_script" || \
            -f "$add_indexes_script" ) ]]
then
    header "Cypher script files missing"
    exit 1
fi

# Check for the presence of the cypher-shell
which cypher-shell > /dev/null
verify_result "cypher-shell not available. Exiting..."

# Loading the companies in the graph
header "Loading companies..."
cat "$add_comp_script" | cypher-shell
verify_result "Failed to load the companies in the graph."

# Loading the universities in the graph
header "Loading universities..."
cat "$add_uni_script" | cypher-shell
verify_result "Failed to load the universities in the graph."

# Load the indexes
header "Load indexes..."
cat "$add_indexes_script" | cypher-shell
verify_result "Failed to load the indexes."

# Loading the reviews in the graph
header "Loading reviews..."
cat "$add_rev_script" | cypher-shell
verify_result "Failed to load the reviews in the graph."

# Loading the affiliations in the graph
header "Loading affiliations..."
# Creating the CSV file
python "$add_aff_python"
verify_result "Failed to create the affiliations CSV."

# Load the csv into neo4j
header "Importing affiliations... This may require some time!"
mv "$aff_csv" "$NEO4J_IMPORT"
verify_result "Failed to move the affiliations CSV in the import folder."
cat "$add_aff_script" | cypher-shell
verify_result "Failed to load the affiliations in neo4j."

header "Neo4j extended succesfully!"

