from flask import Flask,render_template,request
import pickle

app=Flask(__name__)

pt=pickle.load(open("pt.pkl",'rb'))
pt_sim=pickle.load(open("pt_sim.pkl","rb"))
books=pickle.load(open("books.pkl","rb"))


@app.route("/")
def index():
    return "hello world"

@app.route("/popular_movie")
def popular():
    with open("famous_books.pkl","rb")as f:
     dt=pickle.load(f)
    return render_template("index.html",
                           book_name=list(dt["Book-Title"].values),
                           author=list(dt["Book-Author"].values),
                           image=list(dt["Image-URL-M"].values),
                           votes=list(dt["num_rating"].values),
                           rating=list(dt["average_rating"].values))


@app.route("/recommend")
def recommend():
     return render_template("recommend.html")

@app.route("/recommend_book",methods=["post"])
def recomend_book():
   data=request.form.get("book")

#    return dt
   
   def recommend(x):
        row=pt.index
        lst=row.to_list()
        near_books_idx=pt_sim[lst.index(x)].tolist()
        data=list(zip(lst,near_books_idx))
        data=sorted(data,key=lambda x:x[1],reverse=True)
        dt=[]
        for book in data[1:6]:
            x=books[books["Book-Title"]==book[0]].iloc[0][["Book-Title","Book-Author","Image-URL-M"]].values
            dt.append(list(x))
        return dt

   top_books=recommend(data)
#    return data
   return render_template("recommend.html",top=top_books)
  
#    dt=request.get_data("book")

   

if __name__=="__main__":
    app.run(debug=True)