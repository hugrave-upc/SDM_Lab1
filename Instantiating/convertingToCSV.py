import json, random, codecs, os
from faker import Faker
fake = Faker()

import numpy as np

# Global config variables
sep_value = '\t'
array_sep = '|'
companies_number = 1000
mean, std = 4, 2

journal_papers_string = open('./sources/journal_papers.json', 'r').read()
conferences_string = open('./sources/conferences.json', 'r').read()

# Extracting the list of all journal papers
journal_papers_json = json.loads(journal_papers_string)['result']['hits']['hit']

# Exctracting the list of all conferences
conferences_json = json.loads(conferences_string)['result']['hits']['hit']

# Creating data structures

authors = set()
volumes = set()
years = set()
journals = set()
articles = []
articleID = 1
conferences = set()
editions = {}
proceedings = {}
cities = set()
keywords = set()
randomCities = ['Brussels','Madrid', 'Barcelona', 'Paris', 'London', 'Rome', 'Lisbon', 'Amsterdam', 'Copenhagen', 'Berlin', 'Stockholm', 'Hamburg', 'Manchester']
keywordsComm = ['data management', 'indexing', 'data modeling', 'big data', 'data', 'processing', 'data storage', 'data querying']
randomKeywords = ['Software', 'Hardware', 'TCP/IP','ROM','RAM', 'security policy', 'model simple security condition', 'star property', 'asterisk-property',
                'mathematical model', 'secure computer system', 'security', 'trusted subject']

randomKeywords = \
['Big data', 'Databases', 'Data modeling', 'Data storage', 'Semantic data'] + \
['IOT', 'Sensors', 'Real time', 'Streams', 'Connection'] + \
['Cybersecurity', 'Protocols', 'Tokens', 'Authentication', 'Encryption'] + \
['Bioinformatics', 'Genetic programming', 'Biology', 'DNA', 'Cancer'] + \
['Quantum', 'Physics', 'QBit', 'Combinatorics', 'Entanglement'] + \
['AI', 'Machine Learning', 'Classification', 'Deep Learning', 'Clustering']


# Creating relations

writes = []
vol_contains = []
publishes = set()
in_year_vol = set()
proc_contains = []
has_an = set()
occurs_in = {}
creates = []
in_year_ed = set()
has = set()
cites = set()
reviews = set()
article_year = {}


# Extending data structures
reviewsSummary = []


# JOURNALS

# Nodes

for jp in journal_papers_json:
    journal_paper = jp['info']

    # Creating article
    article_title = journal_paper['title']
    articles.append(str(articleID) + sep_value + article_title + '\n')
    articleID += 1

    # Creating journal
    journal = journal_paper['venue']
    journals.add(journal + '\n')

    # Creating volume
    volume = array_sep.join([journal, journal_paper['volume']])
    volumes.add(volume + '\n')

    # Creating year
    year = journal_paper['year']
    years.add(year + '\n')
    article_year[articleID] = year

    # Creating author
    journal_authors = journal_paper['authors']
    corresponding = 0

    if isinstance(journal_authors['author'], list):
        for author in journal_authors['author']:
            authors.add(author + '\n')
            # Writes: Author -> Article
            # adding corresponding author in relationship
            if corresponding == 0:
                writes.append(sep_value.join([author, 'Yes', str(articleID - 1) + '\n']))
                corresponding = 1
            else:
                writes.append(sep_value.join([author, 'No', str(articleID-1) + '\n']))
    else:
        author = journal_authors['author']
        authors.add(author + '\n')
        # Writes: Author -> Article
        writes.append(sep_value.join([author, 'Yes', str(articleID - 1) + '\n']))

    # Creating keywords
    numberWords = int(np.random.normal(mean, std))
    while numberWords > 0:
        secure_random = random.SystemRandom()
        keyword = secure_random.choice(randomKeywords)
        keywords.add(keyword + '\n')
        # Has = article -> keyword
        has.add(sep_value.join([str(articleID - 1), keyword + '\n']))
        numberWords -= 1




# Edges

    # Vol_contains: volume -> article
    pages = journal_paper['pages']
    vol_contains.append(sep_value.join([volume, pages, str(articleID-1) + '\n']))

    # Publishes: journal -> volume
    publishes.add(sep_value.join([journal, year, volume + '\n']))

    # In_year_vol: volume -> year
    in_year_vol.add(sep_value.join([volume, year + '\n']))


# CONFERENCES

# Nodes

for conf in conferences_json:
    conf_paper = conf['info']

    # Creating articles
    article_title = conf_paper['title']
    articles.append(sep_value.join([str(articleID), article_title + '\n']))
    articleID += 1

    # Creating conferences
    conference = conf_paper['key'].split('/')[1]
    conferences.add(conference + '\n')

    # Creating edition and city
    ed_key = str(2019 - int(conf_paper['year']) + 1)
    edition = conference+str(ed_key)

    #Add city:
    if edition not in editions:
        secure_random = random.SystemRandom()
        city = secure_random.choice(randomCities)
        cities.add(city + '\n')
        # Occurs_in: edition -> city
        occurs_in[edition] = sep_value.join([edition, city + '\n'])

    # Add edition
    editions[edition] = sep_value.join([edition, str(ed_key) + '\n'])

    # Creating author
    conf_authors = conf_paper['authors']
    corresponding = 0

    if isinstance(conf_authors['author'], list):
        for author in conf_authors['author']:
            authors.add(author + '\n')


            # Writes: Author -> Article
            # adding corresponding author in relationship
            if corresponding == 0:
                writes.append(sep_value.join([author, 'Yes', str(articleID - 1) + '\n']))
                corresponding = 1
            else:
                writes.append(sep_value.join([author, 'No', str(articleID-1) + '\n']))
    else:
        author = conf_authors['author']
        authors.add(author + '\n')
        # Writes: Author -> Article
        writes.append(sep_value.join([author, 'Yes', str(articleID - 1) + '\n']))

    # Creating years
    year = conf_paper['year']
    years.add(year + '\n')
    article_year[articleID] = year

    # Creating keywords
    numberWords = int(np.random.normal(mean, std))
    while numberWords > 0:
        secure_random = random.SystemRandom()
        keyword = secure_random.choice(randomKeywords)
        keywords.add(keyword + '\n')
        # Has = article -> keyword
        has.add(sep_value.join([str(articleID - 1), keyword + '\n']))
        numberWords -= 1

# Edges

    # Proc_contains: edition -> article
    proc_contains.append(sep_value.join([edition, pages, str(articleID-1) + '\n']))

    # Has_an: conference -> edition
    has_an.add(sep_value.join([conference, year, edition + '\n']))

    # In_year_ed
    in_year_ed.add(sep_value.join([edition, year + '\n']))




def addReviewsSummary(article_id, reviewers):
    negativeBallot = bool(random.getrandbits(1))
    if negativeBallot:
        negative_reviewer = reviewers.pop(0)
        reviewsSummary.append(sep_value.join([negative_reviewer, article_id, 'Rejected', ' '.join(fake.text().splitlines()) + '\n']))
    for reviewer in reviewers:
        reviewsSummary.append(sep_value.join([reviewer, article_id, 'Approved', ' '.join(fake.text().splitlines()) + '\n']))



# Creating citations and reviewers
articleID = 1
for artInfo in journal_papers_json + conferences_json:
    article = artInfo['info']
    article_id = str(articleID)
    numCitation = random.randint(2,10)
    secure_random = random.SystemRandom()

    # Adding reviewers

    numReviewers = 3
    reviewers = []
    while numReviewers > 0:
        reviewer = secure_random.sample(authors,1)[0].replace('\n', '')
        if isinstance(article['authors']['author'], list):
            if reviewer not in article['authors']['author']:
                reviews.add(sep_value.join([reviewer, article_id + '\n']))
                reviewers.append(reviewer)
                numReviewers -= 1
        else:
            if reviewer != article['authors']['author']:
                reviews.add(sep_value.join([reviewer, article_id + '\n']))
                reviewers.append(reviewer)
                numReviewers -= 1
    addReviewsSummary(article_id, reviewers)

    # Adding citations
    while numCitation > 0:
        cited = secure_random.choice(articles).split(sep_value)[0]
        if article_id != cited and int(cited) in article_year and article['year'] >= article_year[int(cited)]:
            cites.add(sep_value.join([article_id, cited + '\n']))
            numCitation -= 1

    articleID += 1

# Creating random companies
if not os.path.isfile('./out_csv/companies.csv'):
    companies = []
    for idx in range(0, companies_number):
        companies.append(sep_value.join([fake.company(), random.choice(randomCities) + '\n']))


# Creating CSVs

with codecs.open('./out_csv/articles.csv', 'w', encoding='utf-8') as f:
    f.write(sep_value.join(['articleID:ID(Article)', 'title\n']))
    f.writelines(articles)

with codecs.open('./out_csv/authors.csv', 'w', encoding='utf-8') as f:
    f.write('name:ID(Author)\n')
    f.writelines(authors)

with codecs.open('./out_csv/writes.csv', 'w', encoding='utf-8') as f:
    f.write(sep_value.join([':START_ID(Author)', 'corresponding_author', ':END_ID(Article)\n']))
    f.writelines(writes)

with codecs.open('./out_csv/journals.csv', 'w', encoding='utf-8') as f:
    f.write(sep_value.join(['journalID:ID(Journal)', 'title\n']))
    f.writelines(journals)

with codecs.open('./out_csv/vol_contains.csv', 'w', encoding='utf-8') as f:
    f.write(sep_value.join([':START_ID(Volume)', 'pages', ':END_ID(Article)\n']))
    f.writelines(vol_contains)

with codecs.open('./out_csv/volumes.csv', 'w', encoding='utf-8') as f:
    f.write('volumeID:ID(Volume)\n')
    f.writelines(volumes)

with codecs.open('./out_csv/publishes.csv', 'w', encoding='utf-8') as f:
    f.write(sep_value.join([':START_ID(Journal)', 'year', ':END_ID(Volume)\n']))
    f.writelines(publishes)

with codecs.open('./out_csv/in_year_vol.csv', 'w', encoding='utf-8') as f:
    f.write(sep_value.join([':START_ID(Volume)', ':END_ID(Year)\n']))
    f.writelines(in_year_vol)

with codecs.open('./out_csv/years.csv', 'w', encoding='utf-8') as f:
    f.write('number:ID(Year)\n')
    f.writelines(years)

with codecs.open('./out_csv/conferences.csv', 'w', encoding='utf-8') as f:
    f.write('name:ID(Conference)\n')
    f.writelines(conferences)

with codecs.open('./out_csv/editions.csv', 'w', encoding='utf-8') as f:
    f.write(sep_value.join(['proceeding:ID(Edition)', 'number\n']))
    f.writelines(editions.values())

with codecs.open('./out_csv/cities.csv', 'w', encoding='utf-8') as f:
    f.write('name:ID(City)\n')
    f.writelines(cities)

with codecs.open('./out_csv/proc_contains.csv', 'w', encoding='utf-8') as f:
    f.write(sep_value.join([':START_ID(Edition)', 'pages', ':END_ID(Article)\n']))
    f.writelines(proc_contains)

with codecs.open('./out_csv/has_an.csv', 'w', encoding='utf-8') as f:
    f.write(sep_value.join([':START_ID(Conference)', 'year', ':END_ID(Edition)\n']))
    f.writelines(has_an)

with codecs.open('./out_csv/occurs_in.csv', 'w', encoding='utf-8') as f:
    f.write(sep_value.join([':START_ID(Edition)', ':END_ID(City)\n']))
    f.writelines(occurs_in.values())

with codecs.open('./out_csv/in_year_ed.csv', 'w', encoding='utf-8') as f:
    f.write(sep_value.join([':START_ID(Edition)', ':END_ID(Year)\n']))
    f.writelines(in_year_ed)

with codecs.open('./out_csv/keywords.csv', 'w', encoding='utf-8') as f:
    f.write('name:ID(Keyword)\n')
    f.writelines(keywords)

with codecs.open('./out_csv/has.csv', 'w', encoding='utf-8') as f:
    f.write(sep_value.join([':START_ID(Article)', ':END_ID(Keyword)\n']))
    f.writelines(has)

with codecs.open('./out_csv/cites.csv', 'w', encoding='utf-8') as f:
    f.write(sep_value.join([':START_ID(Article)', ':END_ID(Article)\n']))
    f.writelines(cites)

with codecs.open('./out_csv/reviews.csv', 'w', encoding='utf-8') as f:
    f.write(sep_value.join([':START_ID(Author)', ':END_ID(Article)\n']))
    f.writelines(reviews)

with codecs.open('./out_csv/reviews_summary.csv', 'w', encoding='utf8') as f:
    f.write(sep_value.join(['Reviewer', 'ArticleID', 'Decision', 'Description\n']))
    f.writelines(reviewsSummary)

if not os.path.isfile('./out_csv/companies.csv'):
    with open('./out_csv/companies.csv', 'w') as f:
        f.write(sep_value.join(['Company name', 'City\n']))
        f.writelines(companies)

