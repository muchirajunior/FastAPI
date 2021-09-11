from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from shortuuid import uuid

app=FastAPI()

client=MongoClient("mongodb://127.0.0.1:27017/todoDb")
db=client.todosDb
collection=db['collection']

class Todo(BaseModel):
    _id:str
    title:str
    name: str
    description: str
    complete: bool

def serializer(todo) -> dict:
    return {
        "_id":str(todo["_id"]),
        "title":todo["title"],
        "name": todo["name"],
        "description": todo["description"],
        "complete":todo["complete"]
    }

def multi_serializer(todos) -> list:
    return [serializer(todo) for todo in todos]
        

@app.get('/')
def index():
    print(client)
    return {"state":"running"}

# crud
# crete todo method 1
@app.post('/create')
def createTodo(todo:Todo):
    newTodo={
       "_id":uuid() 
    }
    newTodo.update(todo)
    collection.insert_one(newTodo)

    return newTodo

# create todo method 2
@app.post('/add_todo')
def addTodo(todo:dict):
    todo['_id']=uuid()
    collection.insert_one(todo)

    return todo

@app.post('/create_many')
async def createMany(todos:list):
    for todo in todos:
        todo['_id']=uuid()
    collection.insert_many(todos)

    return {"message":"success","todos":todos}

@app.get('/todo/{todoId}')
def getTodo(todoId:str):
    todo=collection.find_one({"_id":todoId})

    return {"message":"success","todo":todo}
    

@app.get('/todos')
def getData():
    data=collection.find()
    todos=[]
    # todos=multi_serializer([todo for todo in data])
    for todo in data:
        todos.append(todo)

    return todos

# update todo
@app.put('/update')
async def updateTodo(todo:dict):
    collection.find_one_and_update({"_id":todo["_id"]}, {"$set":todo})
    
    return {"message":"success"}

# replace or change a todo
@app.put('/replace')
async def replace(todo:dict):
    collection.find_one_and_replace({"_id":todo["_id"]},todo)

    return {"message":"success"}

# delete one todo
@app.delete('/delete/{todoId}')
async def deleteTodo(todoId:str):
    collection.find_one_and_delete({"_id":todoId})

    return {"message":"success"}

# delete_many todos
@app.delete('/delete_many/{title}')
async def deleteMany(title:str):
    collection.delete_many({"title":title})

    return {"message":"success"}
    