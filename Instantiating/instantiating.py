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
editions = {}
ed_key = 0

# Creating relations

writes = []
split_into = []
has_a = set()
#written_by = set()
published = set()
hasAn = set ()

#Add into structures

for jp in journal_papers_json:
    journal_paper = jp['info']
    journal_authors = journal_paper['authors']
    article_title = journal_paper['title']
    journal = journal_paper['venue']
    volume = journal_paper['volume']
    year = journal_paper['year']

    #Handles multiple authors
    if isinstance(journal_authors['author'], list):
        for author in journal_authors['author']:
            authors.add(author + '\n')
            writes.append(author + ',' + article_title + '\n')
            #written_by.add(journal + ',' + author + '\n')
    else:
        authors.add(journal_authors['author'])

    articles.add(article_title + '\n')
    journals.add(journal + '\n')
    split_into.append(volume + ',' + article_title + '\n')
    volumes.add(volume + '\n')
    has_a.add(journal + ',' + volume + '\n')
    years.add(year + '\n')
    published.add(volume + ',' + year + '\n')


#CONFERENCES

# Exctracting the list of all conferences
conferences_json = json.loads(conferences_string)['result']['hits']['hit']

# Creating relations

groups = []

for conf in conferences_json:
    conf_paper = conf['info']
    conf_authors = conf_paper['authors']
    article_title = conf_paper['title']
    edition = conf_paper['venue']
    if edition in editions :
        edition = editions.edition
    else:
        editions[edition] = ed_key
        edition = ed_key
        ed_key += 1

    conf = conf_paper['key'].split('/')[1]

    year = conf_paper['year']

    if isinstance(conf_authors['author'], list):
        for author in conf_authors['author']:
            authors.add(author + '\n')
            writes.append(author + ',' + article_title + '\n')

    else:
        authors.add(conf_authors['author'])

    articles.add(article_title + '\n')
    conferences.add(conf + '\n')
    #groups.append(article_title + ',' + conf + '\n')
    years.add(year + '\n')





with open('./articles.csv', 'w') as f:
    f.writelines(articles)

with open('./authors.csv', 'w') as f:
    f.writelines(authors)

with open('./writes.csv', 'w') as f:
    f.writelines(writes)

with open('./journals.csv', 'w') as f:
    f.writelines(journals)

with open('./splitInto.csv', 'w') as f:
    f.writelines(split_into)

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

#with open('./isPartOf.csv', 'w') as f:
    #f.writelines(is_part_of)




