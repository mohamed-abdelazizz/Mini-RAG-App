from pydantic import BaseModel, Field
from typing import Optional


class ProcessRequest(BaseModel):
    file_id: Optional[str] = Field(default=None)
    chunk_size: Optional[int] = Field(default=100, gt=0)
    overlap_size: Optional[int] = Field(default=20, ge=0)
    do_reset: Optional[int] = Field(default=0, ge=0, le=1)  # if you have the same file and want to reset(remove all the old), set this to 1
    # do_something => do to indicate that this param will be used to do an action
