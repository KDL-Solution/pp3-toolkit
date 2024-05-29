from requests import Session, exceptions
import os
from PIL import Image
import io
from requests_toolbelt import MultipartEncoder

def login_and_create_session(id="admin", pw="admin1234", base_url="https://api.polyground.info/", endpoint="v1/auth/login"):
    """
    사용자 ID와 비밀번호를 이용해 로그인하고, 반환된 토큰과 쿠키를 세션 헤더에 저장.

    Args:
    - url (str): 로그인 API의 URL 주소
    - id (str): 사용자 ID
    - pw (str): 사용자 비밀번호

    Returns:
    - session (requests.Session): 인증 정보가 포함된 세션 객체
    """
    url = os.path.join(base_url, endpoint)
    session = Session()
    data = {
        "loginId": id,
        "password": pw,
        "authType": "POLYGROUND"
    }
    res = session.post(url, json=data)
    
    res.raise_for_status()
    
    token = res.json().get("token")
    cookies = res.cookies
    cookie_header = '; '.join([f"{key}={value}" for key, value in cookies.items()])

    session.headers.update({'Authorization': f'Bearer {token}', 'Cookie': cookie_header})
    print("Successfully logged in")
        
    return session


def reissue(session:Session, base_url="https://api.polyground.info/", endpoint="v1/auth/reissue"):
    """
    세션으로 토큰 재발급 요청.
    새로운 토큰으로 세션의 인증 헤더를 업데이트. (기존 토큰 갱신)

    Args:
    - session (requests.Session): 현재 유효한 세션 객체
    - url (str): 토큰 재발급 API의 URL 주소

    Returns:
    - session (requests.Session): 업데이트된 세션 객체
    """
    url = os.path.join(base_url, endpoint)
    res = session.patch(url)
    res.raise_for_status()
    token = res.json().get("token")
    session.headers.update({'Authorization': f'Bearer {token}'})

def reissue_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exceptions.HTTPError as e:
            if e.response.status_code == 401:
                session = args[0]
                reissue(session)
                return func(*args, **kwargs)
            else:
                raise e
    return wrapper

@reissue_decorator
def get_resource_content_public(session:Session, resource_id, base_url="https://api.play.polyground.ai", endpoint="v1/resource/public"):
    """
    public resource 에 ID를 통해 파일을 바이너리 형태로 받음.

    Args:
    - session (requests.Session): 인증 정보가 포함된 세션 객체
    - resource_id (str): 고유 ID
    - url (str): public resource API의 URL 주소

    Returns:
    - content (bytes): 파일의 바이너리 데이터
    """ 
    url = os.path.join(base_url, endpoint, str(resource_id))
    res = session.get(url)
    res.raise_for_status()
    return res.content

@reissue_decorator
def upload_resource_public(session:Session, name, file_buffer, mime_type="image/jpeg", base_url="http://api.play.polyground.ai", endpoint="v1/resource/public"):
    """
    파일을 멀티파트 형식으로 서버에 업로드.
    파일의 이름, 데이터, 타입을 이용하여 멀티파트 요청을 구성하고 전송.

    Args:
    - session (requests.Session): 인증 정보가 포함된 세션 객체
    - name (str): 업로드할 파일의 이름
    - file_buffer (bytes): 파일 데이터
    - mime_type (str): 파일의 MIME 타입 (기본값은 "image/jpeg")
    - url (str): 파일 업로드 API의 URL 주소

    Returns:
    - res (requests.Response): 요청 결과를 담은 응답 객체
    """
    url = os.path.join(base_url, endpoint)
    m = MultipartEncoder(
        fields={'file': (name, file_buffer, mime_type)}
    )
    headers = {
        'Accept': 'application/json',
        'Content-Type': m.content_type
    }
    res = session.post(url, data=m, headers=headers)
    res.raise_for_status()
    return res

def read_image(content):
    """
    바이너리 형태의 이미지 데이터를 NumPy 배열로 변환하여 이미지로 읽음.

    Args:
    - content (bytes): 이미지 파일의 바이너리 데이터

    Returns:
    - img (numpy.ndarray): 변환된 이미지 데이터
    """
    # nparr = np.frombuffer(content, np.uint8)
    # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    image_stream = io.BytesIO(content)
    img = Image.open(image_stream)
    return img

def array_to_buffer(array):
    """
    array 형태의 이미지 데이터를 바이너리 형태로 변환.
    
    Args:
    - array (numpy.ndarray): 이미지 데이터
    
    Returns:
    - buffered (bytes): 이미지 데이터의 바이너리 형태
    """
    image = Image.fromarray(array[:,:,::-1])

    # 이미지를 바이트 스트림으로 변환
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return buffered.getvalue()

if __name__ == "__main__":
    session = login_and_create_session()
    content = get_resource_content_public(session,  1)
    img = read_image(content)
    

    # 이미지 업로드 예시
    # res = upload_resource_public(session,"1c0e6d73176a50e81f5d96c0de73547a.jpg", array_to_buffer(img), mime_type="image/jpeg")
    # print(res.json())
    # # 토큰 갱신
    # reissue(session)
    
    img.save("result.jpg")
    