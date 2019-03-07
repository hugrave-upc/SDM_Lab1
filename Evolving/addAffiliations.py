# Extending the graph with the reviews

from neo4j import GraphDatabase

import random

uri = 'bolt://localhost:7687'
driver = GraphDatabase.driver(uri, auth=('', ''))

sep_value = '\t'

# Extracting all the authors
def get_authors(tx):
    authors = tx.run("match (a:Author) return a.name as name;")
    return authors

# Extracting all the companies
def get_companies(tx):
    companies = tx.run("match (c:Company) return c.name as name;")
    return companies

# Extracting all the universities
def get_universities(tx):
    universities = tx.run("match (u:University) return u.name as name;")
    return universities



with driver.session() as session:
    authors = session.read_transaction(get_authors)
    companies = session.read_transaction(get_companies)
    universities = session.read_transaction(get_universities)
    comp_list = list(companies)
    uni_list = list(universities)

    print(len(comp_list), len(uni_list))
affiliations = set()
for author in authors:
    isCompany = bool(random.getrandbits(1))
    if isCompany:
        affiliations.add(sep_value.join([author['name'], random.choice(comp_list)['name'], 'Company\n']))
    else:
        affiliations.add(sep_value.join([author['name'], random.choice(uni_list)['name'], 'University\n']))

with open('./out_csv/affiliations.csv', 'w') as f:
    f.write(sep_value.join(['author', 'institution name', 'Company|University\n']))
    f.writelines(affiliations)
