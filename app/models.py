from pydantic import BaseModel, Field


class DiagnoseRequest(BaseModel):
    incident: str = Field(min_length=1, max_length=12000)


class Citation(BaseModel):
    chunk_id: str
    filename: str
    section_title: str


class Step(BaseModel):
    instruction: str
    citations: list[Citation]


class DiagnoseResponse(BaseModel):
    summary: str
    remediation_steps: list[Step]
    citations: list[Citation]
    covered: bool


class IngestResponse(BaseModel):
    files: int
    chunks: int
