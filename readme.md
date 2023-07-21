# Setup Procedure:
1. Create virtual environment (python -m venv env)
2. Active V.Env (source/bin(linux) or script(windows))/activate
3. cd documentManagement(project name)
4. run pip install -r requirements.txt
5. run project python manage.py runserver

## task 1 .User Authentication and Authorization

description: In user Authentication, i used django build in auth system when is_superuser(build in) can manage all the documents
1. you registered user using following api 
    http://127.0.0.1:8000/api/v1/registration/
   (see postman or swagger document)
note: If are registered as admin please provide is_superuser (optional) field
2. You can log in and get access token for authentication
http://127.0.0.1:8000/api/v1/login/
(see postman or swagger document)

## task 2 :Document Management

description: Create a model with necessary field
### permissions:
1. User who create document, can perform all curd operations
2. Admin user can perform all curd operations for all the document to manage
3. Other users who shared documents, can only see the document details and download files
4. Unauthenticated user can't perform any operations
   (You can see all the api endpoints in swagger or import postman json file given)

## task 3 :Document Upload
description: User can upload document but it has different some rules 
1. Document must be following formats
   ('.pdf', '.jpg', '.jpeg', '.png', '.gif', '.doc', '.docx')
2. Document size not more than 5mb
Only Auth user can upload documents
(You can see all the api endpoints in swagger or import postman json file given)

## task 4 :Document Download
description: User can download own's documents or those shared with him
Admin can download all documents
I provide all the permission for documents downloading 
(You can see all the api endpoints in swagger or import postman json file given)

## task 5 : Sharing
description: User can share documents with others
(You can see all the api endpoints in swagger or import postman json file given)

## task 6 :Search
description: User can search his documents using it's Search title, description, format, or 
upload date
(You can see all the api endpoints in swagger or import postman json file given)

## task 7 : Documentation
I documented all api's using swagger and postman both

## task 8 : Bonus Points
I also implement a feature to convert documents from one format to another (e.g., from docx 
to pdf)
Implement version control, so users can keep track of changes to their documents over 
time
(You can see all the api endpoints in swagger or import postman json file given)