from neo4j import GraphDatabase


uri = 'bolt://localhost:7687'
driver = GraphDatabase.driver(uri, auth=('', ''))


def create_an_author(tx):
    result = tx.run("LOAD CSV FROM "
                    "'https://raw.githubusercontent.com/hugrave-upc/SDM_Lab1/master/Instantiating/authors.csv' "
                    "AS line FIELDTERMINATOR ','"
                    "CREATE (:Author { name: line[0]})")
    print(result)


def create_an_article(tx):
    result = tx.run("LOAD CSV FROM "
                    "'https://raw.githubusercontent.com/hugrave-upc/SDM_Lab1/master/Instantiating/articles.csv' "
                    "AS line FIELDTERMINATOR ','"
                    "CREATE (:Article { title: line[0]})")
    print(result)


def create_writes(tx):
    result = tx.run("LOAD CSV FROM "
                    "'https://raw.githubusercontent.com/hugrave-upc/SDM_Lab1/master/Instantiating/writes.csv' "
                    "AS line FIELDTERMINATOR ','"
                    "match (auth:Author), (art:Article) "
                    "where auth.name = line[0] "
                    "and art.title = line[1]"
                    "create (auth)-[r:Writes]->(art) "
                    "return r")
    print(result)


with driver.session() as session:
    session.read_transaction(create_writes)
