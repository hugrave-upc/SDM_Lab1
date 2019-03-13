# SDM Lab 1 - Property graphs in Neo4j

This file wants to be an explanatory reference to the project repository. It is divided in folders containing the different sections of the laboratory.
Each one of them contains a shell script which automates the execution of the corresponding section.

## Requirements
**The sources are availabale in GitHub, they were not inserted in the compressed folder due to space reason.**

Repository: https://github.com/hugrave-upc/SDM_Lab1

A list of python packages are required for the correct execution of the following scripts.
```bash
pip install Faker neo4j numpy unicodecsv
```
The code has been tested on **Python 2.7**.

## Instantiating

The main script for this section is the *convertingToCSV.py* file. However, since it is using the *neo4j-admin import* utility, it requires to reset the database every time. 
In order to make the process smooth, we created a shell script to automate it. Running *import.sh* the database is stopped, deleted, loaded and restarted. However, a problem is encountered all the times Neo4j is restarted. (TODO)
Whenever the database needs to be reset without generating the CSV files again, the following command can be executed:
```bash
import.sh --no-csv 
```

## Evolving
In order to evolve the graph, several Cypher queries need to be executed.
The program *neo4j_evolve.sh* can be executed. It executes through Python or *cypher-shell* all the queries needed.

## Queries
The program *neo4j_queries.sh* needs two arguments: the query number to be executed and the the limit of rows that the user wants to display.
Example:
```bash
./neo4j_queries.sh 1 10
```
The example above runs the first query displaying only the first 10 lines.

## Graph algorithms
The program *neo4j_graphAlgo.sh* builds the co-authorship relations, clusters the authors and run the queries.
If the relations are already created, the **skip** parameter can be specified.
```bash
./neo4j_graphAlgo.sh [skip]
```

## Reccomender
In order to produce the right recommendations, several information need to be materialized.
Through the *neo4j_reccommender.sh* it is possible to execute all the steps and then, through a user interface, request for the top authors.
However, since the program may be run several times, it is possible to pass the option *skip* to to avoid the materialization of the previous steps.
```bash
./neo4j_reccommender.sh [skip]
```