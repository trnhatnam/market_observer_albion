import re
import pandas as pd

regex = re.compile(r"\s*\d+:\s*(\w*)@?(\w*)\s*:?\s*(.*)\n")
df = pd.DataFrame(columns=["nom"])
df.index.name = "identifiant"

with open("items.txt") as f:
	while True:
		line = f.readline()
		if line=="":
			break
		rematch = regex.match(line)
		identifiant,_,nom = rematch.groups()
		if _ == '' and nom != '':
			df.loc[identifiant] = nom
		

df.to_csv("items.csv")

