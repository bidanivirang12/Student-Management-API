from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field,computed_field,EmailStr
from fastapi.responses import JSONResponse
from typing import Optional,Annotated
import json



#defining the pydantic model for data validation
class Student(BaseModel): #id will be auto-generated
    name: str
    grade: str
    age: int
    email: EmailStr 

#loading data
def load_data():
    with open ("student.json","r") as f:
        data=json.load(f)
        return data

def save_data(data):
    with open("student.json","w") as f:
        json.dump(data,f,indent=4)


app=FastAPI(
    title="Student Management API"
)
#Introduction page
@app.get("/",tags=["Students"])
def student():
    return {"This is a Student Management API"}

#For Inserting data
@app.post("/students", tags=["Students"])
def insert_student(student:Student):
    data=load_data()
    
#Generate Student id
    if data["students"]:
        new_id= max(s["id"] for s in data["students"]) + 1
        #data["students"] goes through list of students
        #s["id"] goes through every student id
        #max gives the highest id number and +1 generates the next id
    else:
        new_id=1
    #conversion of pydantic model to dictioanry
    new_student=student.model_dump()
    new_student["id"]=new_id
    #append this data to the list
    data["students"].append(new_student)
    #save the new student
    save_data(data)

    return JSONResponse(status_code=201,content={"message":"Patient Created successfully"}
    )


    #This is the case if we use temp storage students[]
    #converting the validated pydantic model to a dictionary
        # new_student=student.model_dump()
    #generating an auto id system
    # new_student["id"] = len(students) + 1
    # #saves the student to the existing file which is temp storage
    # students.append(new_student)

    return JSONResponse(status_code=200, content={"message":'Student created successfully'})

@app.get("/students/{id}",tags=["Students"])
def get_student(id: int):
    data=load_data()
#Loop through every student
#Comparestudent id with the target id
#if they match return
#Else give an HTTP error
#the line below tells python that for each student from students in the data save one at a time in a var called "student"
    for student in data["students"]:
        if student["id"]==id:
            return student
    raise HTTPException(status_code=404,detail='Patient Not Found')

    
    
    
    #This is the case if we use temp storage students[]
    # for student in students:
    #     if student["id"]==id:
    #         return student
    # raise HTTPException(status_code=404, detail="Student not found")

@app.get("/all_students",tags=["Students"])
def get_students():
    data=load_data()
    return data

    #This is the case if we use temp storage students[]
    # return students