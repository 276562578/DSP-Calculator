from flask import Flask, render_template, request
import json

app = Flask(__name__)
with open("recipes.json", "r", encoding="utf-8") as f:
    recipes = json.load(f)

def get_recipes_item_in(item,num):
    item_recipes = []
    for i in recipes[item]:
        producer=i["producer"]
        items_in = []
        items_out=[]

        for m in i["out"]:
            if m["name"]==item:
                out_num=m["num"]
        in_multi=num/out_num

        for n in i["in"]:
            n["num"]=num/out_num*n["num"]
            items_in.append(n)

        for k in i["out"]:
            k["num"]=num/out_num*k["num"]
            items_out.append(k)

        item_recipes.append({"producer":producer,
                             "in":items_in,
                             "out":items_out})

    return item_recipes

@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route("/get_item_in", methods=["POST"])
def get_item_in():
    item_out=request.form["item_out"]
    out_num=request.form["out_num"]
    results = get_recipes_item_in(item_out, int(out_num))
    for a in results:
        print("In producer:")
        print(a["producer"])
        print("you need item: ")
        for m in a["in"]:
            print(m["name"],m["num"])
        print("you will get: ")
        for n in a["out"]:
            print(n["name"],n["num"])
    return render_template("output.html",results=results)


if __name__ == '__main__':
    app.run()
