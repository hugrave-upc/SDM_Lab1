import json
import random


journal_papers_string = open('./journal_papers.json', 'r').read()
conferences_string = open('./conferences.json', 'r').read()

#JOURNALS

# Exctracting the list of all journal papers
journal_papers_json = json.loads(journal_papers_string)['result']['hits']['hit']

# Creating data structures

authors = set()
volumes = set()
years = set()
journals = set()
articles = set()
conferences = set ()
editions = set ()

# Creating relations

writes = []
belongs_to = []
has_a = set()
written_by = set()
published = set()
hasAn = set ()

for jp in journal_papers_json:
    journal_paper = jp['info']
    journal_authors = journal_paper['authors']
    article_title = journal_paper['title']
    journal = journal_paper['venue']
    volume = journal_paper['volume']
    year = journal_paper['year']

    if isinstance(journal_authors['author'], list):
        for author in journal_authors['author']:
            authors.add(author + '\n')
            writes.append(author + ',' + article_title + '\n')
            written_by.add(journal + ',' + author + '\n')
    else:
        authors.add(journal_authors['author'])

    articles.add(article_title + '\n')
    journals.add(journal + '\n')
    belongs_to.append(article_title + ',' + journal + '\n')
    volumes.add(volume + '\n')
    has_a.add(journal + ',' + volume + '\n')
    years.add(year + '\n')
    published.add(volume + ',' + year + '\n')


#CONFERENCES

# Exctracting the list of all conferences
conferences_json = json.loads(conferences_string)['result']['hits']['hit']

# Creating relations

is_part_of = []

for conf in conferences_json:
    conf_paper = conf['info']
    conf_authors = conf_paper['authors']
    article_title = conf_paper['title']
    conf = conf_paper['venue']
    year = conf_paper['year']

    if isinstance(conf_authors['author'], list):
        for author in conf_authors['author']:
            authors.add(author + '\n')
            writes.append(author + ',' + article_title + '\n')

    else:
        authors.add(conf_authors['author'])

    articles.add(article_title + '\n')
    conferences.add(conf + '\n')
    is_part_of.append(article_title + ',' + conf + '\n')
    years.add(year + '\n')

    #create editions
for c in conferences:
    edi = random.randint(1,3)



with open('./articles.csv', 'w') as f:
    f.writelines(articles)

with open('./authors.csv', 'w') as f:
    f.writelines(authors)

with open('./writes.csv', 'w') as f:
    f.writelines(writes)

with open('./journals.csv', 'w') as f:
    f.writelines(journals)

with open('./belongsTo.csv', 'w') as f:
    f.writelines(belongs_to)

with open('./volumes.csv', 'w') as f:
    f.writelines(volumes)

with open('./hasA.csv', 'w') as f:
    f.writelines(has_a)

with open('./writtenBy.csv', 'w') as f:
    f.writelines(written_by)

with open('./years.csv', 'w') as f:
    f.writelines(years)

with open('./published.csv', 'w') as f:
    f.writelines(published)

with open('./conferences.csv', 'w') as f:
    f.writelines(conferences)

with open('./isPartOf.csv', 'w') as f:
    f.writelines(is_part_of)

#


