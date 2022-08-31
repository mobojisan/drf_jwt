from urllib import response
from django.test import TestCase, Client

from shop.models import Book

# TODO: 拡張: テスト対象は何か?, クライアントテストどうやってやるか
# TODO: templatesを直す＋リモートあげる -> 時間枠予約
class TestHoge(TestCase):
    def test_create(self):
        book = Book.objects.create(
            title="dd",
            price=400,
            created_at="2022-08-23T02:50:43.526Z",
        )
        
        self.assertEqual(Book.objects.filter(title="dd").exists(), True)

    def test_list_api(self):
        response = Client().get(
            '/api/v1/books/',
        ),
        content_type='application/json',
        # 取得したトークンを設定
        HTTP_AUTHORIZATION=f"Bearer {access_token}"
        
        print(response.content)
        print(response.status_code)
