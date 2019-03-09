
from neo4j import GraphDatabase

uri = 'bolt://localhost:7687'
driver = GraphDatabase.driver(uri, auth=('', ''))

topAuthors = """
match (c:Community)-[:Top]->(:Article)<-[:Writes]-(auth:Author)
with c.name as Community, collect(distinct auth.name) as distinctTopAuthors, collect(auth.name) as TopAuthors
unwind distinctTopAuthors as topAuthor
with Community, topAuthor, size([a in TopAuthors where a=topAuthor]) as PapersWritten
with Community, topAuthor, (case when PapersWritten > 1 then 'Guru' else 'Influencing' end) as Status
with Community, Status, collect(topAuthor) as topAuthors
return Community, collect({Category: Status, Authors: topAuthors}) as TopAuthors;
"""


def get_communities(tx):
    result = tx.run("match(c:Community) return c.name as name;")
    return result

def get_top_authors(tx):
    return tx.run(topAuthors)

with driver.session() as session:
    communities = session.read_transaction(get_communities)
    topAuthors = session.read_transaction(get_top_authors)
    for ta in topAuthors:
        print ('===============')
        print (ta['Community'])
        print('\n'.join([x['Category'] + ' -> ' + ', '.join(x['Authors']) for x in ta['TopAuthors']]))
        print('')

    #print ('\n'.join([tp['Community'] + ' - ' + ', '.join(['(' + ta['Article'] + ', ' + str(ta['score']) + ')' for ta in tp['TopArticles']]) for tp in topPapers]))