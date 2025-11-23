import numpy as np 
import pandas as pd

books=pd.read_csv("Books.csv")
rate=pd.read_csv("Ratings.csv")
user=pd.read_csv("Users.csv")

# print(books.info())
# print(rate.info())
# print(user.info())

#no duplicate, only age ,issing value

#ratings have some books which is not in books so rows decrea
df=pd.merge(books,rate,on="ISBN")
# print(df.shape)


# print(df.isnull().sum())

#now here we want every book average rating 
# print(df.info())
# num_df=df.groupby("Book-Title").count()["Book-Rating"].reset_index()
# print(type(num_df))
# num_df.rename()
pop_df=df.groupby("Book-Title")["Book-Rating"].aggregate(["count","mean"]).reset_index()
# print(avrage_Rating)
pop_df.rename(columns={"count":"num_rating","mean":"average_rating"},inplace=True)

pop_df=pop_df[pop_df["num_rating"]>=250]
pop_df.sort_values(by="average_rating",ascending=False,inplace=True)
pop_df=pop_df.head(50)
pop_df=pop_df.merge(books,on="Book-Title")
pop_df.drop_duplicates("Book-Title",inplace=True)
pop_df=pop_df[["Book-Title","average_rating","Book-Author","num_rating","Image-URL-M"]]

print(pop_df["Image-URL-M"][0])

# print(pop_df.values)
# import pickle
#   let's import the pickle file
### code had remove just 2 lines 


#collabrative fikt user rates more than 200 times  and books with more than rating 50 
# NOTE:get the user index with rating given more than 200 times and the books with more than equals to 50 ratings
cnt_df=df.groupby("User-ID").count()["Book-Title"]

#group by k baad "User-ID" ban jayega index

#user rate more than 200 books
idx=cnt_df[cnt_df>200].index
filter_rating=df[df["User-ID"].isin(idx)]


#books with more than 50 ratings 
cp=filter_rating.groupby("Book-Title").count()["Book-Rating"]
famous_books=cp[cp>=50].index
filter_rating=filter_rating[filter_rating["Book-Title"].isin(famous_books)]

# print(filter_rating)


# NOW WE WANT A PIVOT TABLE 
pt=filter_rating.pivot_table(index="Book-Title",columns="User-ID",values="Book-Rating")
pt.fillna(0,inplace=True)
# print(pt)?


#find near vector and we will have cosine similarity

# print()
from sklearn.metrics.pairwise import cosine_similarity

pt_sim=cosine_similarity(pt)

print(type(pt_sim))

# print(
#     books.info()
# )

def recommend(x):
    row=pt.index
    lst=row.to_list()
    near_books_idx=pt_sim[lst.index(x)].tolist()
    # print(near_books_idx)
    data=list(zip(lst,near_books_idx))
    data=sorted(data,key=lambda x:x[1],reverse=True)
    # print(data[1:6])
    dt=[]
    for book in data[1:6]:
        x=books[books["Book-Title"]==book[0]].iloc[0][["Book-Title","Book-Author","Image-URL-M"]].values
        dt.append(list(x))
    print(dt)

    

recommend("1984")


#this recommend function, pt_sim and by importing it 

import pickle
with open("books.pkl","wb") as f:
    pickle.dump(books,f)

with open("pt_sim.pkl","wb") as f:
    pickle.dump(pt_sim,f)

with open("pt.pkl","wb") as f:
    pickle.dump(pt,f)