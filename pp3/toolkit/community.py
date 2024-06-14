from pp3.toolkit.auth import token_reissue_decorator
from requests import Session
import os
from enum import Enum

class ModelType(str, Enum):
  TTI = "TTI"
  ITI = "ITI"
  IT3 = "IT3"
  TT3 = "TT3"
  ITV = "ITV"
  TTV = "TTV"

@token_reissue_decorator
def register_model(
      session: Session,
      name: str,
      type: ModelType,
      title: str,
      description: str,
      url: str,
      path: str = "/",
      health: str = "/health",
      base_url="https://api.play.polyground.ai",
      endpoint="v1/community/generate/register",
    ):
    community_url = os.path.join(base_url, endpoint)

    payload = {
      "identifier": name,
      "type": type.value,
      "title": title,
      "description": description,
      "url": url,
      "paths": {
        "request": path,
        "health": health
      }
    }
    response = session.post(community_url, json=payload)
    
    response.raise_for_status()

@token_reissue_decorator
def deregister_model(
      session: Session,
      name:str,
      base_url="https://api.play.polyground.ai",
      endpoint="v1/community/generate/deregister",
    ):
   
    community_url = os.path.join(base_url, endpoint, name)
    response = session.delete(community_url)

    response.raise_for_status()