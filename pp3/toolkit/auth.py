from requests import Session, exceptions
import os

def login(
    user_id: str, 
    password: str,
    auth_type: str = "POLYGROUND",
    base_url="https://api.polyground.info/", 
    endpoint="v1/auth/login",
    verify=False
    )-> Session:
    """
    사용자 ID와 비밀번호를 이용해 로그인하고, 반환된 토큰과 쿠키를 세션 헤더에 저장하여 초기화된 세션 객체를 반환합니다.

    Args:
    - user_id (str): 사용자 ID
    - password (str): 사용자 비밀번호
    - auth_type (str): 인증 타입 (기본값은 "POLYGROUND")
    - base_url (str): Auth API 서버의 기본 URL
    - endpoint (str): 로그인 API의 엔드포인트

    Returns:
    - session (requests.Session): 인증 토큰과 쿠키가 포함된 세션 객체
    """
    login_url = os.path.join(base_url, endpoint)
    session = Session()
    session.verify = verify # SSL 인증서 검증 여부
    login_payload = {
        "loginId": user_id,
        "password": password,
        "authType": auth_type
    }
    response = session.post(login_url, json=login_payload)
    
    response.raise_for_status() # 에러 발생시 예외 발생
    
    token = response.json().get("token")
    cookies = response.cookies
    cookie_header = '; '.join([f"{key}={value}" for key, value in cookies.items()])

    session.headers.update({'Authorization': f'Bearer {token}', 'Cookie': cookie_header})
    print("Successfully logged in.")
        
    return session


def update_session_token(
    session: Session, 
    base_url="https://api.polyground.info/", 
    endpoint="v1/auth/reissue"
    ) -> None:
    """
    현재 세션의 토큰을 재발급 받고, 인증 헤더를 업데이트합니다.

    Args:
    - session (requests.Session): 현재 유효한 세션 객체
    - base_url (str): Auth API 서버의 기본 URL
    - endpoint (str): 토큰 재발급 API의 엔드포인트

    Returns:
    - session (requests.Session): 업데이트된 세션 객체
    """
    reissue_url = os.path.join(base_url, endpoint)
    response = session.patch(reissue_url)
    response.raise_for_status()
    new_token = response.json().get("token")
    session.headers.update({'Authorization': f'Bearer {new_token}'})

def token_reissue_decorator(func):
    """
    토큰 만료(401 Unauthorized) 에러 발생 시 자동으로 토큰을 재발급 받고 함수를 재시도하는 데코레이터.

    Args:
    - func (Callable): 토큰을 사용하여 API 요청을 하는 함수

    Returns:
    - Callable: 토큰 재발급 로직이 적용된 함수
    """
    
    def wrapper(*args, **kwargs):
        session = args[0]
        try:
            return func(*args, **kwargs)
        except exceptions.HTTPError as e:
            if e.response.status_code in [401, 403]:
                update_session_token(session)
                return func(*args, **kwargs)
            raise
    return wrapper