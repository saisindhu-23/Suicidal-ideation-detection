import firebase_admin
from firebase_admin import credentials, db
import json

with open('appsettings.json', 'r') as json_file:
    appsettings = json.load(json_file)

API_KEY_PATH = "key.json"

certificate = credentials.Certificate(API_KEY_PATH) 
firebaseApp = firebase_admin.initialize_app(certificate, {'databaseURL': appsettings['DatabaseURL']})

class ToDoCollection():
    def addTodoItem(self, content):
        if self.key in content:
            if not self.__findItem(content[self.key]):
                self.collection.push(content)
                return True
            else:
                raise Exception("Item already exists")
        else:
            raise Exception("Key {0} not found".format(self.key))
    
    def getTodoItem(self,id):
        todoList = self.getTodoItems()
        todoItem = next((item for item in todoList if item[self.key] == id), None)
        return todoItem