from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse

from schemas import paper as paper_schema
from services import paper as paper_service

router = APIRouter()

'''
POST   /paper/request       # Submit paper link
GET    /paper/status/{id}   # Check generation status (pending, done, error)
GET    /paper/script/{id}   # Get podcast-style script
GET    /paper/audio/{id}    # Stream or download audio
'''

tasks = dict()


@router.post("/request", status_code=status.HTTP_202_ACCEPTED)
def request_paper_generation(paper: paper_schema.PaperBase) -> StreamingResponse:
    """
    Submit a paper link for processing.
    This endpoint will accept a paper link and initiate the generation process.
    """
    return paper_service.stream_generate_podcast(paper.link)


@router.get("/task/{task_id}")
def get_task(task_id):
    return paper_service.get_task(task_id)
