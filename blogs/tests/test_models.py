from django.test import TestCase
from blogs.models import Category, Tag, PostModel

# Create your tests here
class PostModelTestCase(TestCase):
    def setUp(self):
        category = Category.objects.create(name='slack', slug='slack')
        PostModel.objects.create(title='A New title', category=category)
    
    def test_post_model(self):
        obj = PostModel.objects.get(pk=1)
        self.assertEqual(obj.title, 'A New title')
        self.assertTrue(obj.content == None)
        self.assertEqual(str(obj), obj.title)
    
class TagTestCase(TestCase):
    def test_tag_model(self):
        tag = Tag.objects.create(name='slack', slug='slack')
        self.assertEqual(str(tag), tag.name)
    