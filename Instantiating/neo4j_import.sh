#!/bin/bash


verify_result() {
    if [ $? -ne 0 ]; then
        echo $1
        exit 1
    fi
}

## Stopping neo4j service
echo "Stopping neo4j service..."
service neo4j stop
verify_result "Failed to stop neo4j server"

## Running the CSV generation script
echo "Creating the CSV files... This may require several minutes!"
python convertingToCSV.py
verify_result "Failed to convert sources to CSV"


## Importing the CSV in the db
echo "Importing the files in neo4j..."

which neo4j-admin
verify_result "neo4j-admin could not be found"

rm -rf /var/lib/neo4j/data/databases/dblp.db

neo4j-admin import --mode=csv --database=dblp.db --delimiter "TAB" --id-type string \
--nodes:Author "out_csv/authors.csv" \
--nodes:Article "out_csv/articles.csv" \
--nodes:City "out_csv/cities.csv" \
--nodes:Conference "out_csv/conferences.csv" \
--nodes:Edition "out_csv/editions.csv" \
--nodes:Journal "out_csv/journals.csv" \
--nodes:Keyword "out_csv/keywords.csv" \
--nodes:Volume "out_csv/volumes.csv" \
--nodes:Year "out_csv/years.csv" \
--relationships:Cites "out_csv/cites.csv" \
--relationships:Has "out_csv/has.csv" \
--relationships:Has_an "out_csv/has_an.csv" \
--relationships:In "out_csv/in_year_ed.csv" \
--relationships:In "out_csv/in_year_vol.csv" \
--relationships:Occurs_in "out_csv/occurs_in.csv" \
--relationships:Contains "out_csv/proc_contains.csv" \
--relationships:Publishes "out_csv/publishes.csv" \
--relationships:Reviews "out_csv/reviews.csv" \
--relationships:Contains "out_csv/vol_contains.csv" \
--relationships:Writes "out_csv/writes.csv"
verify_result "Error importing the data"

chown neo4j /var/lib/neo4j/data/databases/dblp.db

## Starting neo4j service
echo "Starting neo4j service..."
service neo4j start