import pandas as pd
import pickle
df=pd.read_csv("cars_images.csv")
Brand=df.car.tolist()
logo=df.image.tolist()
imgs={}
for i in range(len(Brand)):
    imgs[Brand[i]]=logo[i]
pickle.dump(imgs,open("cars_images.pkl","wb"))