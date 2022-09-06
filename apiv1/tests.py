from urllib import response
from django.test import TestCase, Client
from rest_framework_simplejwt.tokens import RefreshToken
from shop.models import Book
from django.conf import settings

# TODO: 拡張: テスト対象は何か?, クライアントテストどうやってやるか

class TestHoge(TestCase):

    # ここ
    fixtures = [
        'initial.json',
    ]

    def setUp(self) -> None:
        settings.REST_FRAMEWORK['PAGE_SIZE'] = 1

    def tearDown(self) -> None:
        settings.REST_FRAMEWORK['PAGE_SIZE'] = 100

    def test_create(self):
        book = Book.objects.create(
            title="dd",
            price=400,
            created_at="2022-08-23T02:50:43.526Z",
        )
        
        self.assertEqual(Book.objects.filter(title="dd").exists(), True)

    def test_list_api(self):
        refresh = Client().post(
            '/api/v1/auth/jwt/create/',
            data={
                'username': 'root',
                'password': 'toor',
            }
        )
        import json
        # print(json.dumps(refresh.json(), indent=4))
        # print(refresh.__dict__)
        response = Client().get(
            '/api/v1/books/',
            content_type='application/json',
            # 取得したトークンを設定
            HTTP_AUTHORIZATION=f"Bearer {refresh.json().get('access')}",
        )
        # pretty-print
        # print(json.dumps(response.json(), indent=4))
        # print(result.content)
        # print(response.status_code)
        self.assertEqual(response.status_code, 200)
        
        def test_filter(self):
            pass
