from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.database import db_connection 

app = FastAPI()  # Here app is server application which covers all things


# Data validation using Pydantic
class TakeSchema(BaseModel):
    id: int
    text: str
    completed: bool = False

        
@app.get("/tasks")  # Decorator + HTTP Method + Path
def get_all_tasks():
    cursor=None
    connection=None
    try:
        connection = db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM tasks")
        all_tasks = cursor.fetchall()

        

        return {"status": "success", "data": all_tasks}
    except Exception:
        raise HTTPException(status_code=500,detail="Internal server error")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()    


@app.post("/tasks")
def create_task(new_task: TakeSchema):
    connection = None
    cursor = None

    try:
        connection = db_connection()
        cursor = connection.cursor()

        take_dict = new_task.model_dump()

        cursor.execute(
            "SELECT * FROM tasks WHERE id=%s",
            (take_dict["id"],)
        )

        exist_id = cursor.fetchone()

        if exist_id:
            raise HTTPException(
                status_code=400,
                detail="Task ID already exists!"
            )

        query = """
        INSERT INTO tasks(id, text, completed)
        VALUES(%s, %s, %s)
        """

        values = (
            take_dict["id"],
            take_dict["text"],
            int(take_dict["completed"])
        )

        cursor.execute(query, values)
        connection.commit()

        return {
            "status_submitted": "success",
            "added_data": take_dict
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.put("/tasks/{new_id}")
def update_task(new_id: int, update_task: TakeSchema):
    connection = None
    cursor = None

    try:
        connection = db_connection()
        cursor = connection.cursor()

        updated_task = update_task.model_dump()

        query = """
        UPDATE tasks
        SET text=%s, completed=%s
        WHERE id=%s
        """

        values = (
            updated_task["text"],
            int(updated_task["completed"]),
            new_id
        )

        cursor.execute(query, values)
        connection.commit()

        return {
            "status": "submitted successfully",
            "Added data": updated_task
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.delete("/tasks/{new_id}")
def delete_task(new_id: int):
    connection = None
    cursor = None

    try:
        connection = db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM tasks WHERE id=%s",
            (new_id,)
        )

        connection.commit()

        return {
            "status": "Delete successful"
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Query Parameters for searching
@app.get("/tasksfind")
def get_search_tasks(search: str = None):
    connection = None
    cursor = None

    try:
        connection = db_connection()
        cursor = connection.cursor()

        if not search:
            cursor.execute("SELECT * FROM tasks")
            all_task = cursor.fetchall()

            return {
                "status": "Success",
                "Data": all_task
            }

        query = "SELECT * FROM tasks WHERE text LIKE %s"

        search_value = (f"%{search}%",)

        cursor.execute(query, search_value)

        filtered_task = cursor.fetchall()

        return {
            "status": "successful",
            "Found_data": filtered_task
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()