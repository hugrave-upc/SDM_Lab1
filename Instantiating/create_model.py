from neo4j import GraphDatabase

uri = 'bolt://localhost:7687'
driver = GraphDatabase.driver(uri, auth=('', ''))


def create_an_author(tx, name) :
    query = "create (n:Author {name: {name}})"
    tx.run(query, name=name)

def create_an_article(tx, name) :
    query = "create (n:Article {name: {name}})"
    tx.run(query, name=name)

def create_write_rel(tx, author, article) :
    result = tx.run("match (auth:Author), (art:Article) "
        "where auth.name = {author} "
        "and art.name = {article} "
        "create (auth)-[r:Writes]->(art) "
        "return r",
        author=author, article=article)

    print(result)

    
with driver.session() as session :
    session.read_transaction(create_write_rel, 'Sara', 'The best students in BDMA')



with driver.session() as session :
    session.read_transaction(create_write_rel, 'Sara', 'The best students in BDMA')