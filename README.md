\# Task API



A small CRUD API for managing a to-do list, built with FastAPI. Built as part of \[Backend AI Engineering/https://internship.flyrank] — this is a learning project with in-memory storage only, no database.



\## How to run it



1\. Clone this repo and enter the folder:

&#x20;  git clone https://github.com/favour79/todo-api.git

&#x20;  cd todo-api



2\. Create and activate a virtual environment:

&#x20;  python -m venv venv

&#x20;  venv\\Scripts\\activate      (Windows)

&#x20;  source venv/bin/activate   (Mac/Linux)



3\. Install dependencies:

&#x20;  pip install fastapi uvicorn



4\. Run the server:

&#x20;  uvicorn main:app --reload



5\. Open http://localhost:8000/docs to see and test the API in Swagger UI.



\## Endpoints



| Method | Path              | Description                          |

|--------|-------------------|---------------------------------------|

| GET    | /                 | API info                              |

| GET    | /health           | Health check                          |

| GET    | /tasks            | List all tasks                        |

| GET    | /tasks/{task\_id}  | Get one task by id                    |

| POST   | /tasks            | Create a new task                     |

| PUT    | /tasks/{task\_id}  | Update a task's title and/or done     |

| DELETE | /tasks/{task\_id}  | Delete a task                         |



\## Example request



curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\\"title\\":\\"Buy milk\\"}"



Response:

HTTP/1.1 201 Created

{"id":4,"title":"Buy milk","done":false}



\## Swagger UI



Screenshot below shows a successful POST /tasks call tested directly in Swagger UI:



!\[Swagger screenshot](swagger-screenshot.png)



\## Notes



Data is stored in memory only — restarting the server resets the task list back to the 3 example tasks. This is intentional for this stage of the project; persistent storage comes later.

