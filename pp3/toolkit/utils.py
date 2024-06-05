import io
from PIL import Image

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
