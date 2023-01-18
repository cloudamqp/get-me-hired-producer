from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from schemas import JobsQueryModel
from validators import is_valid_email
from cloudamqp_helper import cloudamqp


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/jobs")
async def find_jobs(jobs_query: JobsQueryModel):
    """ Accepts job queries and adds them to RabbitMQ """
    
    email = jobs_query.email
    search_term = jobs_query.search_term
    location = jobs_query.location

    # Verify that all request parameters are passed
    if email is None or search_term is None or location is None:
        return HTTPException(
            detail={'message': 'Error! Pass all request paramaters'}, 
            status_code=400
        )

    # Check if email is valid
    if not is_valid_email(email):
        return HTTPException(
            detail={'message': 'The email passed is not valid!'}, 
            status_code=400
        )

    # Publish request to CloudAMQP
    await cloudamqp.publish_message(
        message_body= {
            "email": email,
            "search_term": search_term,
            "location": location
        }
    )
    
    return ("Your request has been queued, we will email the list"
            " of available jobs to you shortly"
    )