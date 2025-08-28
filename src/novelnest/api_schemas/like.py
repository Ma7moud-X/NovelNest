from pydantic import BaseModel, ConfigDict, field_validator

class LikeToggle(BaseModel):
    piece_id: int
    direction: int = 1  # 1 = like, 0 = unlike (remove)
    
    @field_validator('direction')
    @classmethod
    def validate_direction(cls, v):
        if v not in [0, 1]:
            raise ValueError('direction must be either 0 (unlike) or 1 (like)')
        return v

class Like(BaseModel):
    piece_id: int
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)
    
class LikeCount(BaseModel):
    piece_id: int
    like_count: int