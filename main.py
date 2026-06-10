from fastapi import FastAPI 
from pydantic import BaseModel
app=FastAPI() # Here app is server application which cover all things

class Takeschema(BaseModel):
    id:int
    text:str
    completed:bool=False
todo_list=[{"id":1,"text":"learn fastapi","completed":False},
      {"id":2,"text":"Run server","completed":True}
]    
@app.get("/tasks")  # Decorator + Path + HTTP Method
def get_all_tasks():
    return{"status":"success","data":todo_list}
@app.post("/tasks")
def create_task(new_task:Takeschema):
    take_dict=new_task.model_dump()
    for item in todo_list:
        if item["id"] == take_dict["id"]:
            
            return {"status": "error", "message": f"Task with ID {take_dict['id']} already exists!"}
    todo_list.append(take_dict)
    return {"status submitted":"success"," added data":take_dict}
