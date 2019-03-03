#!/bin/bash

which neo4j-admin
if [ $? -ne 0 ]; then
    exit 1
fi

neo4j-admin import --mode=csv --database=dblp.db --delimiter ";" --id-type string \
--nodes:Author "authors.csv" \
--nodes:Article "articles.csv" \
--nodes:City "cities.csv" \
--nodes:Conference "conferences.csv" \
--nodes:Edition "editions.csv" \
--nodes:Journal "journals.csv" \
--nodes:Keyword "keywords.csv" \
--nodes:Volume "volumes.csv" \
--nodes:University "world-universities.csv" \
--nodes:Year "years.csv" \
--relationships:Cites "cites.csv" \
--relationships:Has "has.csv" \
--relationships:Has_an "has_an.csv" \
--relationships:In "in_year_ed.csv" \
--relationships:In "in_year_vol.csv" \
--relationships:Occurs_in "occurs_in.csv" \
--relationships:Contains "proc_contains.csv" \
--relationships:Publishes "publishes.csv" \
--relationships:Reviews "reviews.csv" \
--relationships:Contains "vol_contains.csv" \
--relationships:Writes "writes.csv"
