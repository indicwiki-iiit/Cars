import pickle
DF =pickle.load(open('./data/cars_30k.pkl', 'rb'))
ids = DF.Name.tolist()
versions={}
for i in ids:
	li=i.split("స్పెక్స్:")
	namet_edit=li[0].split(" ")
	namet_str=""
	for i in range(len(namet_edit)):
		if i==0:
			yeart=namet_edit[i]
		else:
			namet_str+=namet_edit[i]+ " "
	model=namet_str[:-1]+yeart
	if(model not in versions):
		versions[model]=[]
		versions[model].append(li[1][1:])
	else:
		versions[model].append(li[1][1:])
file=open("./data/versions_30k.pkl","wb")
pickle.dump(versions,file)