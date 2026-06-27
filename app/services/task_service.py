from fastapi import HTTPException
class Task_service:
    @staticmethod #we use this decoretor due to work with outside data(ex: db)
    def get_all_tasks(db):
        db.execute("SELECT * FROM tasks")
        all_tasks=db.fetchall()
        if all_tasks:
            return all_tasks
        return []