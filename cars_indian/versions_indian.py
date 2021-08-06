import pandas as pd
import pickle
df1=pd.read_csv("./data/cars_indian.csv")
#print(df1)
ids=df1.car_id.tolist()
dict={}
for i in ids:
	row = df1.loc[df1['car_id']==i]
	if(row.Make.values[0]!="#"):
		model=str(row.Make.values[0])+" "+str(row.Model.values[0])
		if model not in dict:
			dict[model]=[]
			dict[model].append(str(row.Make.values[0])+" "+str(row.Model.values[0])+" "+str(row.Variant.values[0]))
		else:
			dict[model].append(str(row.Make.values[0])+" "+str(row.Model.values[0])+" "+str(row.Variant.values[0]))
	else:
		model=row.Model.values[0]
		if model not in dict:
			dict[model]=[]
			dict[model].append(str(row.Model.values[0])+" "+str(row.Variant.values[0]))
		else:
			dict[model].append(str(row.Model.values[0])+" "+str(row.Variant.values[0]))
pickle.dump(dict,open("./data/versions_india.pkl","wb"))

"""def main():
	DF =pickle.load(open('./data/car_data.pkl', 'rb'))
	ids = DF.Name.tolist()
	versions={}
	for i in ids:
		li=i.split("Specs:")
		if(li[0][:-1] not in versions):
			versions[li[0][:-1]]=[]
			versions[li[0][:-1]].append(li[1][1:])
		else:
			versions[li[0][:-1]].append(li[1][1:])
	file=open("versions.pkl","wb")
	pickle.dump(versions,file)
if __name__ == '__main__':
	main()"""