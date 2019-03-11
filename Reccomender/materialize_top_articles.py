import sys
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
with nodeId, score order by score desc
with $CommunityName as Community, collect ({Article: nodeId, score: score})[0..$NumberTopArt] as TopArticles
unwind TopArticles as topArticle
match (art:Article), (c:Community {name: $CommunityName}) where id(art) = topArticle['Article']
merge (art)<-[:Top {score: topArticle['score']}]-(c)
"""


def get_communities(tx):
    result = tx.run("match(c:Community) return c.name as name;")
    return result

def materialize_top_papers(tx, communities):
    for comm in communities:
        tx.run(topArticles.replace('$CommunityName', comm['name'], 1),
               CommunityName=comm['name'],
               NumberTopArt=numberTopArt)

with driver.session() as session:
    communities = session.read_transaction(get_communities)
    session.write_transaction(materialize_top_papers, communities)