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
        # ここに
        # print(response.json())
        # pretty-print
        # print(json.dumps(response.json(), indent=4))
        # print(result.content)
        # print(response.status_code)
        self.assertEqual(response.status_code, 200)
        
    def test_filter(self):
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
            {
                'price__gte': 1000
            },
            content_type='application/json',
            # 取得したトークンを設定
            HTTP_AUTHORIZATION=f"Bearer {refresh.json().get('access')}",
        )
        self.assertEqual(response.json(), { 
            'count': 2,
            'next': None, 
            'previous': None, 
            'results': [
                    {'id': '6e3d5daf-ad3c-40f9-a981-eb4545c1ce33', 'title': 'DRFの教科書', 'price': 2000},
                    {'id': '7334efe9-96f5-4697-b479-55673f9aa098', 'title': 'DRFの教科書', 'price': 2000}
                ]
            }
        )

    def test_page_size(self):
        # refresh = Client().post(
        #     '/api/v1/auth/jwt/create/',
        #     data={
        #         'username': 'root',
        #         'password': 'toor',
        #     }
        # )
        from django.contrib.auth.models import User
        refresh = RefreshToken.for_user(User.objects.get(pk=1))
        access_token = refresh.access_token
        
        import json
        # print(json.dumps(refresh.json(), indent=4))
        # print(refresh.__dict__)
        response = Client().get(
            '/api/v1/books/',
            {
                'page_size': 1,
                'page': 1,
            },
            content_type='application/json',
            # 取得したトークンを設定
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(
            {
                "count": 3,
                "next": "http://testserver/api/v1/books/?page=2&page_size=1",
                "previous": None,
                "results": [
                    {
                        "id": "65f6ac89-fe01-4913-bc9d-6a643b9af14b",
                        "title": "d",
                        "price": 40
                    }
                ]
            },
            response.json()
        )
        response = Client().get(
            '/api/v1/books/',
            {
                'page_size': 1,
                'page': 2,
            }, 
            content_type='application/json',
            # 取得したトークンを設定
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual({'count': 3, 'next': 'http://testserver/api/v1/books/?page=3&page_size=1', 'previous': 'http://testserver/api/v1/books/?page_size=1', 'results': [{'id': '6e3d5daf-ad3c-40f9-a981-eb4545c1ce33', 'title': 'DRFの教科書', 'price': 2000}]}, response.json())
