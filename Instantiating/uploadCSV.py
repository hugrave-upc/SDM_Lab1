from neo4j import GraphDatabase

uri = 'bolt://localhost:7687'
driver = GraphDatabase.driver(uri, auth=('', ''))

#Authors
def create_an_author(tx):
    result = tx.run("LOAD CSV FROM "
                    "'https://raw.githubusercontent.com/hugrave-upc/SDM_Lab1/master/Instantiating/authors.csv' "
                    "AS line FIELDTERMINATOR ','"
                    "CREATE (:Author { name: line[0]})")
    print(result)

#Articles
def create_an_article(tx):
    result = tx.run("LOAD CSV FROM "
                    "'https://raw.githubusercontent.com/hugrave-upc/SDM_Lab1/master/Instantiating/articles.csv' "
                    "AS line FIELDTERMINATOR ','"
                    "CREATE (:Article { title: line[0]})")
    print(result)

#Writes
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

#Journals
def create_a_journal(tx):
    result = tx.run("LOAD CSV FROM "
                    "'https://raw.githubusercontent.com/sdiazben/git_local_repository/master/journals.csv' "
                    "AS line FIELDTERMINATOR ','"
                    "CREATE (:Journal { name: line[0]})")
    print(result)


#Belongs to
def belongs_to(tx):
    result = tx.run("LOAD CSV FROM "
                    "'https://raw.githubusercontent.com/sdiazben/git_local_repository/master/belongsTo.csv'"
                    "AS line FIELDTERMINATOR ','"
                    "match (auth:Article), (art:Journal) "
                    "where auth.title = line[0] "
                    "and art.name = line[1]"
                    "create (auth)-[r:belongsTo]->(art) "
                    "return r")
    print(result)

#Volume
def create_a_volume(tx):
    result = tx.run("LOAD CSV FROM "
                    "'https://raw.githubusercontent.com/sdiazben/git_local_repository/master/volumes.csv' "
                    "AS line FIELDTERMINATOR ','"
                    "CREATE (:Volume { number: line[0]})")
    print(result)


#hasA
def create_has_a(tx):
    result = tx.run("LOAD CSV FROM "
                    "'https://raw.githubusercontent.com/sdiazben/git_local_repository/master/hasA.csv'"
                    "AS line FIELDTERMINATOR ','"
                    "match (auth:Journal), (art:Volume) "
                    "where auth.name = line[0] "
                    "and art.number = line[1]"
                    "create (auth)-[r:hasA]->(art) "
                    "return r")
    print(result)

with driver.session() as session:
    #session.read_transaction(create_an_author)
    #session.read_transaction(create_an_article)
    #session.read_transaction(create_writes)
    #session.read_transaction(create_a_journal)
    #session.read_transaction(belongs_to)
    #session.read_transaction(create_a_volume)
    session.read_transaction(create_has_a)
