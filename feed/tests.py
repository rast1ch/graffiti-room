from django.test import TestCase
from models import Post,Image
from users.models import Author
from django.utils import timezone


class PostTestCase(TestCase):
    def setUp(self):
        author = Author.objects.create(username='test_user', password='test_password')
        Post.objects.create(author=author, slug='123456',
                            description='simple...', uploaded=timezone.now(),
                            active=True,)
    
    def test_post_get_by_slug(self):        
        post = Post.objects.get(slug__exact='123456')
        self.assertEqual(post.description,'simple...')