import json

from neo4j import GraphDatabase

uri = 'bolt://localhost:7687'
driver = GraphDatabase.driver(uri, auth=('', ''))


journal_papers_string = open('./journal_papers.json', 'r').read()

# Exctracting the list of all journal papers
journal_papers_json = json.loads(journal_papers_string)['result']['hits']['hit']


# Creating data structures

authors = set()
volumes = set()
years = set()
journals = set()
articles = set()

# Creating relations

writes = []


for jp in journal_papers_json :
    journal_paper = jp['info']
    journal_authors = journal_paper['authors']
    article_title = journal_paper['title']
    journal = journal_paper['venue']
    volume = journal_paper['volume']
    year = journal_paper['year']

    if isinstance(journal_authors['author'], list) :
        for author in journal_authors['author'] :
            authors.add(author + '\n')
            writes.append(author + ',' + article_title + '\n')
    else :
        authors.add(journal_authors['author'])

    articles.add(article_title + '\n')


with open('./authors.csv', 'w') as f:
    f.writelines(authors)

with open('./articles.csv', 'w') as f:
    f.writelines(articles)

with open('./writes.csv', 'w') as f:
    f.writelines(writes)

def import_authors(tx, authors_csv) :
    tx.run("load csv from {authors_csv} as line "
           "create (:Author {name:line[0]})", authors_csv=authors_csv)

with driver.session() as session :
    session.read_transaction(import_authors, 'authors.csv')


