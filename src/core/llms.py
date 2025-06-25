from mistralai import Mistral
from openai import OpenAI

from core import config

mistral_client = Mistral(api_key=config.MISTRAL_API_KEY)
openai_client = OpenAI(api_key=config.OPENAI_API_KEY)


def get_markdown(pdf_url: str) -> str:
    if pdf_url:
        return _markdown_from_link(pdf_url)
    raise NotImplementedError("Other methods to retrive markdown are not implemented.")


def _markdown_from_link(pdf_url: str) -> str:
    ocr_response = mistral_client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": pdf_url
        },
        include_image_base64=True
    )
    pages = []
    for page in ocr_response.pages:
        pages.append(page.markdown)

    paper = "\n".join(pages)
    return paper


def generate_script(paper: str | None) -> str:
    if not paper:
        return "Cannot generate script"
    summary_response = mistral_client.chat.complete(
        model="mistral-small-2506",
        messages=[
            {
                "role": "user",
                "content": "Generate a podcast style script exaplain the paper with 2 people talking about the paper and asking questions. ",
            },
            {
                "role": "user",
                "content": paper
            }
        ]
    )
    return str(summary_response.choices[0].message.content)
