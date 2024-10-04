from typing import Annotated, Literal, Optional
from pydantic import BaseModel, Field, Strict,Base64Bytes
from constants import *

class Chat(BaseModel):
    message: str
    sender: str


class Message(BaseModel):
    page: Optional[str] = Field(default_page, description="Who sends the error message.")
    mode:Optional[str] = Field(default_mode, description="Who sends the error message.")
    family:Optional[str] = Field(default_model_family, description="Who sends the error message.")

    model:Optional[str] = Field(default_model, description="Who sends the error message.")
    negative_prompt:Optional[str] = Field(default_negative_prompt, description="Who sends the error message.")
    use_for_training:Optional[bool]= Field(default_use_for_training, description="use this for training.")

    message: Optional[str] = Field(None, description="The message to be sent to the model.")
    history: list[Chat] = Field(default_factory=list, description="List of messages to be sent to the model.")    
    intent: Optional[str] = Field(None, description="The intent of the message.")
    entity: Optional[str] = Field(None, description="The entity of the message.")
    patient_id: Optional[str] = Field(None, description="The patient id of the message.")
    patient_ids: Optional[list[str]] = Field(["1"], description="The patient ids of the message.")
    form_data: Optional[str] = Field(None, description="The form data of the message used in auto complete.")




