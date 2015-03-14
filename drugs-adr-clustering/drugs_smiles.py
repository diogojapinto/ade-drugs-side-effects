import adrecs_interface as ai
from chemspipy import ChemSpider
import json

cs = ChemSpider('f1bdf04c-7428-42a1-9530-ffe720c5ec6c')

names = ai.get_all_drugs_names()
drugInformation = {}
i = 1
no = 0
for drug in names:
	print('Searching drug', drug[0], '(', i, 'in', len(names), ')')
	i=i+1
	drugResults = []
	for result in cs.search(drug[0]):
		try:
			drugResults.append({"smiles":result.smiles})
		except AttributeError:
			no = no+1
			print('No smiles', no, 'times')
	drugInformation[drug[0]] = drugResults

fileResults = open('results.json', 'w+')
json.dump(drugInformation,fileResults)
fileResults.close()