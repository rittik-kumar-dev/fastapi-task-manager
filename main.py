from fastapi import FastAPI


from app.routers import tasks

app = FastAPI()  # Here app is server application which covers all things
app.include_router(tasks.router)



        







