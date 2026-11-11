import uuid
from pydantic import BaseModel, Field
from typing import List


class MinimalSource(BaseModel):
    """
    #### class MinimalSource
    \n
    The MinimalSource model represents a single source of information.
    """
    file_path: str
    first_character_index: int
    last_character_index: int
    content: str = Field(default="", exclude=True)


class UnansweredQuestion(BaseModel):
    """
    #### class UnansweredQuestion
    \n
    Represents an unanswered question.
    """
    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str


class AnsweredQuestion(UnansweredQuestion):
    """
    #### class AnsweredQuestion
    \n
    Represents an answered question.
    """
    sources: List[MinimalSource]
    answer: str


class RagDataset(BaseModel):
    """
    #### class RagDataset
    \n
    Represents a dataset of RAG questions.
    """
    rag_questions: List[AnsweredQuestion | UnansweredQuestion]


class MinimalSearchResults(BaseModel):
    """
    #### class MinimalSearchResults
    \n
    Representation of search results.
    """
    question_id: str
    question: str
    retrieved_sources: List[MinimalSource]


class MinimalAnswer(MinimalSearchResults):
    """
    #### class MinimalAnswer
    \n
    Representation of an answer.
    """
    answer: str


class StudentSearchResults(BaseModel):
    """
    #### class StudentSearchResults
    \n
    Representation of minimal search results.
    """
    search_results: List[MinimalSearchResults]
    k: int


class StudentSearchResultsAndAnswer(BaseModel):
    """
    #### class StudentSearchResultsAndAnswer
    \n
    Representation of minimal answer results.
    """
    search_results: List[MinimalAnswer]
    k: int
