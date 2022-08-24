from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from pymongo import MongoClient # Database connector
from bson.objectid import ObjectId # For ObjectId to work
from bson.errors import InvalidId # For catching InvalidId exception for ObjectId
from prometheus_flask_exporter import PrometheusMetrics
import os



mongodb_host = os.environ.get('MONGO_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)    #Configure the connection to the database
db = client.camp2016    #Select the database
todos = db.todo #Select the collection

app = Flask(__name__)


metrics = PrometheusMetrics(app, group_by='endpoint')
counter = metrics.counter(
    'by_endpoint_counter', 'Request count by endpoints',
    labels={'endpoint': lambda: request.endpoint}
)

title = "TODO with Flask"
heading = "ToDo Reminder"
#modify=ObjectId()

def redirect_url():
	return request.args.get('next') or \
		request.referrer or \
		url_for('index')


@app.route("/list")
@counter
def lists ():
	#Display the all Tasks
	todos_l = todos.find()
	a1="active"
	return render_template('index.html',a1=a1,todos=todos_l,t=title,h=heading)

@app.route("/")
@app.route("/uncompleted")
@counter
def tasks ():
	#Display the Uncompleted Tasks
	todos_l = todos.find({"done":"no"})
	a2="active"
	return render_template('index.html',a2=a2,todos=todos_l,t=title,h=heading)


@app.route("/completed")
@counter
def completed ():
	#Display the Completed Tasks
	todos_l = todos.find({"done":"yes"})
	a3="active"
	return render_template('index.html',a3=a3,todos=todos_l,t=title,h=heading)

@app.route("/done")
@counter
def done ():
	#Done-or-not ICON
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})
	if(task[0]["done"]=="yes"):
		todos.update_one({"_id":ObjectId(id)}, {"$set": {"done":"no"}})
	else:
		todos.update_one({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})
	redir=redirect_url()	# Re-directed URL i.e. PREVIOUS URL from where it came into this one

#	if(str(redir)=="http://localhost:5000/search"):
#		redir+="?key="+id+"&refer="+refer

	return redirect(redir)

#@app.route("/add")
#def add():
#	return render_template('add.html',h=heading,t=title)

@app.route("/action", methods=['POST', 'GET'])
@counter
def action ():
	#Adding a Task
	name=request.values.get("name")
	desc=request.values.get("desc")
	date=request.values.get("date")
	pr=request.values.get("pr")
	todos.insert_one({ "name":name, "desc":desc, "date":date, "pr":pr, "done":"no"})
	return redirect("/list")

@app.route("/remove")
@counter
def remove ():
	#Deleting a Task with various references
	key=request.values.get("_id")
	todos.delete_one({"_id":ObjectId(key)})
	return redirect("/")

@app.route("/update")
@counter
def update ():
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})
	return render_template('update.html',tasks=task,h=heading,t=title)

@app.route("/action3", methods=['POST', 'GET'])
@counter
def action3 ():
	#Updating a Task with various references
	name=request.values.get("name")
	desc=request.values.get("desc")
	date=request.values.get("date")
	pr=request.values.get("pr")
	id=request.values.get("_id")
	todos.update_one({"_id":ObjectId(id)}, {'$set':{ "name":name, "desc":desc, "date":date, "pr":pr }})
	return redirect("/")

@app.route("/search", methods=['GET'])
@counter
def search():
	#Searching a Task with various references

	key=request.values.get("key")
	refer=request.values.get("refer")
	if(refer=="id"):
		try:
			todos_l = todos.find({refer:ObjectId(key)})
			if not todos_l:
				return render_template('index.html',a2=a2,todos=todos_l,t=title,h=heading,error="No such ObjectId is present")
		except InvalidId as err:
			pass
			return render_template('index.html',a2=a2,todos=todos_l,t=title,h=heading,error="Invalid ObjectId format given")
	else:
		todos_l = todos.find({refer:key})
	return render_template('searchlist.html',todos=todos_l,t=title,h=heading)

@app.route("/about")
@metrics.do_not_track()
def about():
	return render_template('credits.html',t=title,h=heading)



metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)


if __name__ == "__main__":
	env = os.environ.get('FLASK_ENV', 'development')
	port = int(os.environ.get('PORT', 5000))
	debug = False if env == 'production' else True
	app.run(debug=True)
	app.run(port=port, debug=debug)

# from flask import Flask, render_template,request,redirect,url_for # For flask implementation
# from pymongo import MongoClient # Database connector
# from bson.objectid import ObjectId # For ObjectId to work
# from bson.errors import InvalidId # For catching InvalidId exception for ObjectId
# from prometheus_flask_exporter import PrometheusMetrics
# import os

# mongodb_host = os.environ.get('MONGO_HOST', 'localhost')
# mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
# mongodb_user = os.environ.get('MONGO_USER', 'root')
# mongodb_pass = os.environ.get('MONGO_PASS', 'password')
# if(mongodb_host == 'mongo'):
# 	client = MongoClient(mongodb_host, mongodb_port)
# else:
# 	client = MongoClient("mongodb://" + mongodb_user + ":" + mongodb_pass + "@" + mongodb_host + ":27017") #Configure the connection to the database
# db = client.camp2016    #Select the database
# todos = db.todo #Select the collection

# app = Flask(__name__)
# metrics = PrometheusMetrics(app, group_by='endpoint')
# title = "TODO with Flask"
# heading = "ToDo Reminder"
# #modify=ObjectId()
# common_counter = metrics.counter(
#     'by_endpoint_counter', 'Request count by endpoints',
#     labels={'endpoint': lambda: request.endpoint}
# )
# def redirect_url():
# 	return request.args.get('next') or \
# 		request.referrer or \
# 		url_for('index')

# @app.route("/list", methods=['GET', 'POST'])
# @common_counter
# def lists ():
# 	#Display the all Tasks
# 	todos_l = todos.find()
# 	a1="active"
# 	return render_template('index.html',a1=a1,todos=todos_l,t=title,h=heading)

# @app.route("/")
# @app.route("/uncompleted")
# @common_counter
# def tasks ():
# 	#Display the Uncompleted Tasks
# 	todos_l = todos.find({"done":"no"})
# 	a2="active"
# 	return render_template('index.html',a2=a2,todos=todos_l,t=title,h=heading)


# @app.route("/completed")
# @common_counter
# def completed ():
# 	#Display the Completed Tasks
# 	todos_l = todos.find({"done":"yes"})
# 	a3="active"
# 	return render_template('index.html',a3=a3,todos=todos_l,t=title,h=heading)

# @app.route("/done")
# @common_counter
# def done ():
# 	#Done-or-not ICON
# 	id=request.values.get("_id")
# 	task=todos.find({"_id":ObjectId(id)})
# 	if(task[0]["done"]=="yes"):
# 		todos.update_one({"_id":ObjectId(id)}, {"$set": {"done":"no"}})
# 	else:
# 		todos.update_one({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})
# 	redir=redirect_url()	# Re-directed URL i.e. PREVIOUS URL from where it came into this one

# #	if(str(redir)=="http://localhost:5000/search"):
# #		redir+="?key="+id+"&refer="+refer

# 	return redirect(redir)

# #@app.route("/add")
# #def add():
# #	return render_template('add.html',h=heading,t=title)

# @app.route("/action", methods=['GET', 'POST'])
# @common_counter
# def action ():
# 	#Adding a Task
# 	name=request.values.get("name")
# 	desc=request.values.get("desc")
# 	date=request.values.get("date")
# 	pr=request.values.get("pr")
# 	todos.insert_one({ "name":name, "desc":desc, "date":date, "pr":pr, "done":"no"})
# 	return redirect("/list")

# @app.route("/remove")
# @common_counter
# def remove ():
# 	#Deleting a Task with various references
# 	key=request.values.get("_id")
# 	todos.delete_one({"_id":ObjectId(key)})
# 	return redirect("/")

# @app.route("/update")
# @common_counter
# def update ():
# 	id=request.values.get("_id")
# 	task=todos.find({"_id":ObjectId(id)})
# 	return render_template('update.html',tasks=task,h=heading,t=title)

# @app.route("/action3", methods=['POST'])
# @common_counter
# def action3 ():
# 	#Updating a Task with various references
# 	name=request.values.get("name")
# 	desc=request.values.get("desc")
# 	date=request.values.get("date")
# 	pr=request.values.get("pr")
# 	id=request.values.get("_id")
# 	todos.update_one({"_id":ObjectId(id)}, {'$set':{ "name":name, "desc":desc, "date":date, "pr":pr }})
# 	return redirect("/")

# @app.route("/search", methods=['GET'])
# @metrics.do_not_track()
# def search():
# 	#Searching a Task with various references

# 	key=request.values.get("key")
# 	refer=request.values.get("refer")
# 	if(refer=="id"):
# 		try:
# 			todos_l = todos.find({refer:ObjectId(key)})
# 			if not todos_l:
# 				return render_template('index.html',a2=a2,todos=todos_l,t=title,h=heading,error="No such ObjectId is present")
# 		except InvalidId as err:
# 			pass
# 			return render_template('index.html',a2=a2,todos=todos_l,t=title,h=heading,error="Invalid ObjectId format given")
# 	else:
# 		todos_l = todos.find({refer:key})
# 	return render_template('searchlist.html',todos=todos_l,t=title,h=heading)

# @app.route("/about")
# @metrics.do_not_track()
# def about():
# 	return render_template('credits.html',t=title,h=heading)

# metrics.register_default(
#     metrics.counter(
#         'by_path_counter', 'Request count by request paths',
#         labels={'path': lambda: request.path}
#     )
# )
# if __name__ == "__main__":
# 	env = os.environ.get('FLASK_ENV', 'development')
# 	port = int(os.environ.get('PORT', 5000))
# 	debug = False if env == 'production' else True
# 	app.run(debug=True)
# 	app.run(port=port, debug=debug)
# 	# Careful with the debug mode..
