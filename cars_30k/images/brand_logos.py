import pandas as pd
import pickle
df=pd.read_csv("logos.csv")
Brand=df.Brand.tolist()
logo=df.logo.tolist()
imgs={}
for i in range(len(Brand)):
    imgs[Brand[i]]=logo[i]
pickle.dump(imgs,open("logos.pkl","wb"))