import os, sys
from neo4j import GraphDatabase

uri = 'bolt://localhost:7687'
driver = GraphDatabase.driver(uri, auth=('', ''))

if not sys.argv[1]:
    numberTopArt = 10
else:
    numberTopArt = int(sys.argv[1])

topArticles = """
call algo.pageRank.stream(
	"match (c:Community {name: '$CommunityName'})<--(:Keyword)<--(art:Article)<-[:Contains]-()<--()-[:Related_to]->(c) return id(art) as id",
    "match (a1:Article)-[:Cites]->(a2:Article) return id(a1) as source, id(a2) as target",
    {graph: "cypher"}
)
yield nodeId, score
match (art:Article)
where id(art) = nodeId
with art, score order by score desc
with $CommunityName as Community, collect ({Article: id(art), score: score})[0..$NumberTopArt] as TopArticles
unwind TopArticles as topArticle
match (a:Article)<-[:Writes]-(auth:Author)
where id(a) = topArticle['Article']
with Community, collect(distinct auth.name) as distinctTopAuthors, collect(auth.name) as TopAuthors
unwind distinctTopAuthors as topAuthor
with Community, topAuthor, size([a in TopAuthors where a=topAuthor]) as PapersWritten
with Community, topAuthor, (case when PapersWritten > 1 then 'Guru' else 'Influencing' end) as Status
with Community, Status, collect(topAuthor) as topAuthors
return Community, collect({Category: Status, Authors: topAuthors}) as TopAuthors;
"""


def get_communities(tx):
    result = tx.run("match(c:Community) return c.name as name;")
    return result

def get_top_papers(tx, communities):
    result = []
    for comm in communities:
        result += list(tx.run(topArticles.replace('$CommunityName', comm['name'], 1),
                              CommunityName=comm['name'],
                              NumberTopArt=numberTopArt))
    return result

print ('Getting the top authors...')
with driver.session() as session:
    communities = session.read_transaction(get_communities)
    topPapers = session.read_transaction(get_top_papers, communities)
    for tp in topPapers:
        print ('===============')
        print (tp['Community'])
        print('\n\n'.join([x['Category'] + ' -> ' + ', '.join(x['Authors']) for x in tp['TopAuthors']]))
        print('')

    #print ('\n'.join([tp['Community'] + ' - ' + ', '.join(['(' + ta['Article'] + ', ' + str(ta['score']) + ')' for ta in tp['TopArticles']]) for tp in topPapers]))