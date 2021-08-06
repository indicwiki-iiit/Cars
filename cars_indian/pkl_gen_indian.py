import pandas as pd
import pickle
df=pd.read_csv("./data/cars_indian.csv")
pickle.dump(df,open("./data/cars_india.pkl","wb"))