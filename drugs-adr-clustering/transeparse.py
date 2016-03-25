import pandas as pd
from sklearn import cross_validation

print("Loading data")
matrix_df = pd.read_pickle('data/bipartite_df.p')

print("Creating relations")
rels = [(drug, adr) for drug, adrs in matrix_df.iterrows()
                        for adr, val in adrs.iteritems()
                            if val == 1]

print("Dividing set")
train, test = cross_validation.train_test_split(rels, test_size=0.3)
train, validation = cross_validation.train_test_split(train, test_size=0.3)

print("Full size:", len(rels))
print("Train size:", len(train))
print("Validation size:", len(validation))
print("Test size:", len(test))

def write_to_file(file_name, rel):
    with open(file_name, 'w') as f:
        for drug, adr in rel:
            f.write('{0}\tcauses\t{1}\n'.format(drug, adr))

write_to_file('data/train.txt', train)
write_to_file('data/valid.txt', validation)
write_to_file('data/test.txt', test)
