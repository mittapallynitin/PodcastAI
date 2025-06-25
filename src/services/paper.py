import logging
import time
from uuid import UUID, uuid4

from fastapi.responses import StreamingResponse

from core import llms

logger = logging.getLogger("paper_service")

TASK_STATUS = dict()
TASK_STORE = dict()


class UserTask:
    def __init__(self, uuid: UUID, paper_url: str) -> None:
        self.uuid: UUID = uuid
        self.paper_url: str = paper_url
        self.paper: str | None
        self.summary: str | None
        self.script: str | None
        self.audio: str | None

    def __hash__(self) -> int:
        return hash(self.uuid)

    def __eq__(self, other) -> bool:
        return isinstance(other, UserTask) and self.uuid == other.uuid

    def __str__(self) -> str:
        return str(self.uuid)

    def __repr__(self) -> str:
        return str(self)


def get_task(task_id):
    return TASK_STORE[task_id]


def stream_generate_podcast(paper_link: str) -> StreamingResponse:
    def event_stream(task):
        logger.info("Generating podcast for paper, Task ID: %s ", task)
        yield f"Task ID: {task}\n"

        fetch_paper(task)
        yield "✅ Step 1: Paper fetched successfully\n"

        generate_script(task)
        yield "✅ Step 2: Script generated\n"

        proofread_script(task)
        yield "✅ Step 3: Script proofread\n"

        generate_audio(task)
        yield "✅ Step 4: Audio generated\n"

        TASK_STATUS[task] = "COMPLETED"
        yield f"🎉 Podcast generation completed. Task ID: {task}\n"
    task = UserTask(uuid4(), paper_link)
    TASK_STORE[str(task.uuid)] = task
    return StreamingResponse(event_stream(task), media_type="text/plain")


def fetch_paper(task: UserTask):
    logger.info("Fetching paper from link: %s", task)
    TASK_STATUS[task] = "FETCHING PAPER"
    paper = llms.get_markdown(task.paper_url)
    task.paper = paper


def generate_script(task: UserTask):
    logger.info("Generating script for podcast, %s", task)
    TASK_STATUS[task] = "GENERATING SCRIPT"
    task.script = llms.generate_script(task.paper)
    logger.info("Script generation completed %s", task)


def proofread_script(task: UserTask):
    logger.info("Task: %s, Proofreading script for podcast", task)
    TASK_STATUS[task] = "PROOF READING SCRIPT"
    time.sleep(2)  # Simulate proofreading time
    logger.info("Task: %s, Script proofreading completed", task)


def generate_audio(task: UserTask):
    logger.info("Task: %s, Generating audio for podcast", task)
    TASK_STATUS[task] = "GENERATING AUDIO"
    time.sleep(2)  # Simulate audio generation time
    logger.info("Task: %s, Audio generation completed", task)
    task.audio = "This is the audio"
