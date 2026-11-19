from pydantic import BaseModel, Field


class ProcessRequest(BaseModel):
    file_id: str
    chunk_size: int = Field(default=100, gt=0)
    overlap_size: int = Field(default=20, ge=0)
    do_reset: int = Field(default=0, ge=0, le=1)  # if you have the same file and want to reset(remove all the old), set this to 1
    # do_something => do to indicate that this param will be used to do an action
