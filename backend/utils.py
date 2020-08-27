import time
import jwt
from PIL        import Image
from functools  import wraps

from flask_request_validator import AbstractRule
from flask                   import request, jsonify

from config import SECRET

class DatetimeRule(AbstractRule):

    def validate(self, value):

        """

        결제 완료일 filter 조건으로 들어온 fromDate가
        날짜 형식에 맞는지 확인합니다.

        Args:
            value: query string fromDate

        Returns:
            errors: 날짜 형식이 맞지 않으면 value 를 담은 list
                    유효성 검사를 통과하면 빈 list

        Authors:
            tnwjd060124@gmail.com (손수정)

        History:
            2020-08-27 (tnwjd060124@gmail.com) : 초기 생성

        """

        errors = []

        # 날짜가 8자리가 맞는지 확인 (2020913 이면 error)
        if len(str(value)) != 8:
            errors.append(value)

        return errors

def login_required(func):

    """

    login 이 필요한 요청 시 header에 담긴 access_token을 체크하여
    존재하면 decode하여 user_id를 리턴합니다.

    Returns:
        user_no : access_token 을 decode한 user_no
        400, {'message' : 'KEY_ERROR'} : Token 이 없을 시

    Authors:
        tnwjd060124@gmail.com (손수정)

    History:
        2020-08-27 (tnwjd060124@gmail.com) : 초기 생성

    """

    @wraps(func)
    def wrapper():

        # header Authorization에 담긴 access_token 가져옴
        access_token = request.headers.get('Authorization')

        if access_token:
            # access_token decode
            user_no = jwt.decode(access_token, SECRET['secret_key'], SECRET['algorithm'])['user_no']

            return func(user_no)

        # header에 access_token이 없는경우
        return jsonify({"message" : "UNAUTHORIZED"}), 401

    return wrapper

class ResizeImage:

    """

    이미지를 Large, Medium, Small 사이즈로 resize 한 후, s3에 업로드 합니다.

    Args:
        images:
            {
                'product_image_1' : image 파일,
                'product_image_2' : image 파일,
                'product_image_3' : image 파일,
                'product_image_4' : image 파일,
                'product_image_5' : image 파일
            }

    Returns:
        {
            'product_image_1' : {
                'product_image_L' : Large 사이즈 url,
                'product_image_M' : Medium 사이즈 url,
                'product_image_S' : Small 사이즈 url
            },
            'product_image_2' : {
                'product_image_L' : Large 사이즈 url,
                'product_image_M' : Medium 사이즈 url,
                'product_image_S' : Small 사이즈 url
            },
            'product_image_3' : {
                'product_image_L' : Large 사이즈 url,
                'product_image_M' : Medium 사이즈 url,
                'product_image_S' : Small 사이즈 url
            },
            'product_image_4' : {
                'product_image_L' : Large 사이즈 url,
                'product_image_M' : Medium 사이즈 url,
                'product_image-S' : Small 사이즈 url
            },
            'product_image_5' : {
                'product_image_L' : Large 사이즈 url,
                'product_image_M' : Medium 사이즈 url,
                'product_image-S' : Small 사이즈 url
            }
        }

    Authors:
        tnwjd060124@gmail.com (손수정)

    History:
        2020-08-27 (tnwjd060124@gmail.com) : 초기 생성

    """

    def __init__(self, images):
        self.images         = images
        self.large_width    = 640
        self.medium_width   = 320
        self.small_width    = 150
        self.resize_images  = {}

    def resizing(self):

        for key, values in self.images.items():

            # image 파일 open
            image = Image.open(values)

            # image 사이즈 측정
            width, height = image.size

            # large size로 resizing 하는 메소드 실행
            large_size_image = self.resize_image_to_large(values, width, height)

            # medium size로 resizing 하는 메소드 실행
            medium_size_image = self.resize_image_to_medium(values, width, height)

            # small size로 resizing 하는 메소드 실행
            small_size_image = self.resize_image_to_small(values, width, height)

            # resize_images dictionary에 결과 저장
            self.resize_images[key] = {
                'product_image_L' : large_size_image,
                'product_image_M' : medium_size_image,
                'product_image_S' : small_size_image
            }

    def resize_image_to_large(self, image_file, width, height):

        # image 파일 open
        image = Image.open(image_file)

        # image resize
        image_L = image.resize((self.large_width,int((height*self.large_width)/width)))

        return image_L

    def resize_image_to_medium(self, image_file, width, height):

        # image 파일 open
        image = Image.open(image_file)

        # image resize
        image_M = image.resize((self.medium_width, int((height*self.medium_width)/width)))

        return image_M

    def resize_image_to_small(self, image_file, width, height):

        # image 파일 open
        image = Image.open(image_file)

        # image resize
        image_S = image.resize((self.small_width, int((height*self.small_width)/width)))

        return image_S

    def __call__(self):
        self.resizing()
        return self.resize_images
