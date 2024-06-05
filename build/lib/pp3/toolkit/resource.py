from requests import Session
import os
from requests_toolbelt import MultipartEncoder
from toolkit.auth import token_reissue_decorator

@token_reissue_decorator
def download_public_resource(
    session: Session, 
    resource_id: int, 
    base_url="https://api.play.polyground.ai", 
    endpoint="v1/resource/public"
    ) -> bytes:
    """
    주어진 ID에 해당하는 공개 리소스를 바이너리 형태로 다운로드합니다.

    Args:
    - session (requests.Session): 인증 정보가 포함된 세션 객체
    - resource_id (str): resource의 고유 ID
    - base_url (str): resource API 서버의 기본 URL
    - endpoint (str): public resource를 다운로드하는 API 엔드포인트

    Returns:
    - content (bytes): 파일의 바이너리 데이터
    """ 
    resource_url = os.path.join(base_url, endpoint, str(resource_id))
    response = session.get(resource_url)
    response.raise_for_status()
    return response.content

@token_reissue_decorator
def upload_public_resource(
    session: Session, 
    file_name: str, 
    file_buffer: bytes, 
    mime_type="image/jpeg", 
    base_url="http://api.play.polyground.ai", 
    endpoint="v1/resource/public"):
    """
    파일을 멀티파트 형식으로 서버에 업로드합니다.
    파일 이름, 데이터, MIME 타입을 이용하여 요청을 구성하고 서버로 전송합니다.

    Args:
    - session (requests.Session): 인증 정보가 포함된 세션 객체
    - file_name (str): 업로드할 파일의 이름
    - file_buffer (bytes): 업로드할 파일 데이터
    - mime_type (str): 파일의 MIME 타입 (기본값은 "image/jpeg")
    - base_url (str): 파일 업로드 API의 기본 URL
    - endpoint (str): 파일 업로드 API의 엔드포인트

    Returns:
    - requests.Response: 요청 결과를 담은 응답 객체
    """
    resource_url = os.path.join(base_url, endpoint)
    multipart_encoder = MultipartEncoder(
        fields={'file': (file_name, file_buffer, mime_type)}
    )
    headers = {
        'Accept': 'application/json',
        'Content-Type': multipart_encoder.content_type
    }
    response = session.post(resource_url, data=multipart_encoder, headers=headers)
    response.raise_for_status()
    return response