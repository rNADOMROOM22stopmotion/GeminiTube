from pydantic import BaseModel



class Snippet(BaseModel):
    title : str
    description : str
    categoryId : str = "22"#22
    tags : list[str]
    defaultLanguage : str = "en"
    defaultAudioLanguage : str = "gu-IN"

class Status(BaseModel):
    privacyStatus : str = "public"
    license : str = "youtube"
    selfDeclaredMadeForKids : bool = False


class VideoBody(BaseModel):
    id : str
    snippet: Snippet
    status: Status
