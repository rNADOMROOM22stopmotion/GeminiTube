from pydantic import BaseModel, Field


# -- yotube api stuff --
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
    embeddable : bool = True


class VideoBody(BaseModel):
    id : str
    snippet: Snippet
    status: Status

# -- gemini api stuff --

class GeminiOutput(BaseModel):
    title: str = Field(description='Title of the video, optimized for best CTR but not too different/ changed meaning from original. The title should be english first, then gujarati. title must be less than 100 letters',
                       max_length=100)
    description: str = Field(description='Description of the youtube video. Keep the first paragraph reserved for Ingredients and their quantity. You may use relevent emojis and newline characters after each ingredient. After ingredients, leave 2 new lines and generate a 45-60 paragraph related/ relevent to the video recipe. After that leave 1 more new line and give link to my instagram with required title (e.g. Instagram: https://www.instagram.com/p/CuWxeGhM416/). Finally, leave 3 more new lines and generate about 10 hashtags related to the content optimized for maximum reach.')
    tags: list[str] = Field(description='from the provided titles and description, generate 15 relevent tags for youtube.')

class GeminiInput(BaseModel):
    title: str
    description: str

