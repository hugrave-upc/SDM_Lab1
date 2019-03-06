# Extending the graph with the reviews

reviews_path = '../Instantiating/out_csv/reviews_summary.csv'

with open(reviews_path, 'r') as f:
    header = f.readline()
    reviews = f.readlines()

print(header)
print(reviews[1])

ciao = 'come stai?\nIo bene e tu?\n'
print(' '.join(ciao.splitlines()))