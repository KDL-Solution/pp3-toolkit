import io
import numpy as np
from PIL import Image

def read_image_from_binary(content, return_type="numpy"):
    """
    바이너리 형태의 이미지 데이터를 PIL Image 객체로 변환합니다.

    Args:
    - content (bytes): 이미지 파일의 바이너리 데이터
    - return_type (str): 반환할 데이터 타입 ('numpy' 또는 'PIL'), 기본값은 'numpy')

    Returns:
    - img (PIL.Image.Image or numpy.ndarray): 변환된 이미지 데이터
    """
    image_stream = io.BytesIO(content)
    img = Image.open(image_stream)
    
    return_type = return_type.lower()
    
    if return_type == "numpy":
        return np.array(img)
    elif return_type == "pil":
        return img
    else:
        raise ValueError("return_type은 'numpy' 또는 'PIL'이어야 합니다.")

def convert_array_to_binary(array, format="JPEG"):
    """
    NumPy 배열 형태의 이미지 데이터를 format 형식으로 변환하여 바이너리로 반환합니다.
    
    Args:
    - array (numpy.ndarray): 이미지 데이터
    - format (str): 변환할 이미지 포맷 (기본값은 "JPEG")
    
    Returns:
    - binary (bytes): 이미지 데이터의 바이너리 형태
    """
    image = Image.fromarray(array.astype('uint8'), 'RGB')

    # 이미지를 바이트 스트림으로 변환
    buffered = io.BytesIO()
    image.save(buffered, format=format)
    return buffered.getvalue()
