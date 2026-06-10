
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
app=FastAPI() # Here app is server application which cover all things

class TakeSchema(BaseModel):
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
def create_task(new_task:TakeSchema):
    take_dict=new_task.model_dump()
    for item in todo_list:
        if item["id"] == take_dict["id"]:
            
            return {"status": "error", "message": f"Task with ID {take_dict['id']} already exists!"}
    todo_list.append(take_dict)
    return {"status submitted":"success"," added data":take_dict}
@app.put("/tasks/{new_id}")
def update_task(new_id:int,updated_task:TakeSchema):
    for item in todo_list:
        if item["id"]==new_id:
            item["text"]=updated_task.text
            item["completed"]=updated_task.completed
            return {"status":"update success","updated_data":item}
    raise HTTPException(status_code=404,detail="text not found")


@app.delete("/tasks/{new_id}")
def delete_task(new_id:int):
    for item in todo_list:
        if item["id"]==new_id:
            todo_list.remove(item)
            return { "status":"delete success","message":f"Task with ID {new_id}"}
    raise HTTPException(status_code=404,detail="task not found")    