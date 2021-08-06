import pandas as pd
import pickle
df=pd.read_csv("./data/Brands_final.csv")
Brand=df.Brand.tolist()
data=df.data.tolist()
intro={}
for i in range(len(Brand)):
    intro[Brand[i]]=data[i]
pickle.dump(intro,open("./data/brand_data.pkl","wb"))