# Extending the graph with the reviews

from neo4j import GraphDatabase

uri = 'bolt://localhost:7687'
driver = GraphDatabase.driver(uri, auth=('', ''))

reviews_path = '../Instantiating/out_csv/reviews_summary.csv'
sep_value = '\t'


with open(reviews_path, 'r') as f:
    header = f.readline()
    reviews = f.readlines()


def setReview(tx, fields):
    reviewer = fields[0]
    articleID = fields[1]
    decision = fields[2]
    desc = fields[3]

    result = tx.run("match (:Author {name: {reviewer})-[r:Reviews]->(:Article {articleID: {articleID}}) "
                    "set r.decision = {decision} "
                    "set r.description = {desc};",
                    reviewer=reviewer, articleID=articleID, decision=decision, desc=desc)
    print(result)

for review in reviews:
    fields = review.split(sep_value)

    # Set the property
    with driver.session() as session:
        session.read_transaction(setReview, fields)