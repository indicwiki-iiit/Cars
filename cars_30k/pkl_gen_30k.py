import pandas as pd
import pickle
df=pd.read_csv("./data/cars_30k.csv")
pickle.dump(df,open("./data/cars_30k.pkl","wb"))
