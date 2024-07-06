from flask import Flask,jsonify,request,render_template,redirect,url_for
app=Flask(__name__)
# Initial data in to do list
items=[
    {"id":1,"name":"Item 1","description":"This is item 1"},
    {"id":2,"name":"Item 2","description":"This is item 2"},
    {"id":3,"name":"Item 3","description":"This is item 3"}
]
@app.route('/')
def home():
    return render_template('index.html',items=items)

# To take items from list
@app.route('/items',methods=['GET'])
def get_items():
    return jsonify(items)

# To retrieve items by id
@app.route('/items/<int:item_id>',methods=['GET'])
def get_itembyid(item_id):
    item=next((item for item in items if item["id"]==item_id),None)
    if item is None:
        return jsonify({"Item not found"})
    return jsonify(item)

# To create new task
@app.route('/items', methods=['POST'])
def create_item():
    if request.is_json:
        data = request.json
    else:
        data = request.form
    
    if not data or 'name' not in data:
        return jsonify({"error": "Invalid data"})
    
    new_item = {
        "id": items[-1]["id"] + 1 if items else 1,
        "name": data['name'],
        "description": data.get('description', '')
    }
    items.append(new_item)
    return(redirect(url_for('home')))
    # return jsonify(new_item)

#  Update an existing item
@app.route('/items/<int:item_id>',methods=['PUT'])
def update_item(item_id):
    item=next((item for item in items if item["id"]==item_id),None)
    if item is None:
        return jsonify({"Error, item not found"})
    item['name']=request.json.get('name',item['name'])
    item['description']=request.json.get('description',item['description'])
    return jsonify(item)

# Delete an item
@app.route('/items/<int:item_id>', methods=['POST', 'DELETE'])
def delete_item(item_id):
    global items
    if request.method == 'POST':
        # Check if this is a delete operation
        if request.form.get('_method') == 'DELETE':
            items = [item for item in items if item['id'] != item_id]
            return redirect(url_for('home'))
    elif request.method == 'DELETE':
        items = [item for item in items if item['id'] != item_id]
        return jsonify({"message": "Item deleted"}), 200
    return jsonify({"error": "Invalid method"}), 405


if(__name__=="__main__"):
    app.run(debug=True)