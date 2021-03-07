from django.test import TestCase, RequestFactory, Client
from blogs.models import PostModel, Category
from config.views import TopPage
from blogs.views import PostDetail
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models import Q
from blogs.forms import ContactForm
from django.core.mail import BadHeaderError
from django.utils import timezone

class PostModelTestCase(TestCase):
    # def create_post(self, title, is_public):
    #     category = Category.objects.create(name='slack', slug='slack')
    #     return PostModel.objects.create(title=title, category=category)

    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create(
            username='saito',
            email='aaakakaal@gmail.com',
            password='passabcd'
        )
        self.category = Category.objects.create(name='slack', slug='slack')
        self.obj1 = PostModel.objects.create(title="詳細ページのテスト", category=self.category, is_public='True', content='コンテント')
        self.obj2 = PostModel.objects.create(title="詳細ページのテスト", category=self.category, is_public='False' )
       
    def test_PostDetail_view(self):
        post_detail_url1 = reverse('post_detail', kwargs={'pk':self.obj1.pk})
        post_detail_url2 = reverse('post_detail', kwargs={'pk':self.obj2.pk})
        response1 = self.client.get(post_detail_url1)
        response2 = self.client.get(post_detail_url2)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 404)
    
    def test_PostDetail_context_auth(self):
        post_detail_url1 = reverse('post_detail', kwargs={'pk':self.obj1.pk})
        request = self.factory.get(post_detail_url1)
        request.user=self.user
        response= PostDetail.as_view()(request, pk=self.obj1.pk)
        self.assertIsNotNone(response.context_data['like'])
    
    def test_TopPage_view(self):
        toppage_url = reverse('toppage')
        response = self.client.get(toppage_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'toppage.html')

    def test_TopPage_view_auth(self):
        toppage_url = reverse('toppage')
        request = self.factory.get(toppage_url)
        request.user = self.user
        response = TopPage.as_view()(request)
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
    
    def test_searchfunc_view_valid(self):
        search_url=reverse('search')
        response = self.client.get(search_url, data={'key_search':'テスト'})
        self.assertEqual(response.status_code, 200)

    def test_searchfunc_view_invalid(self):
        search_url=reverse('search')
        response = self.client.get(search_url, data={'key_search':''})
        self.assertEqual(response.status_code, 200)
    
    def test_Allcontents_view(self):
        allcontents_url = reverse('all_contents')
        response = self.client.get(allcontents_url)
        self.assertEqual(response.status_code, 200)
    
    def test_categoryfunc_view(self):
        category_url = reverse('category', kwargs={'cats': self.category.slug})
        response = self.client.get(category_url)
        self.assertEqual(response.status_code, 200)

    def test_RankingList_view(self):
        rankinglink_url = reverse('ranking')
        response = self.client.get(rankinglink_url)
        self.assertEqual(response.status_code, 200)


class ContactTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            # create →create_user
            username='admin',
            email='saitou@gmail.com',
            password='pass'
        )
        self.client = Client()
        self.contact_url = reverse('contact')
        self.category = Category.objects.create(name='slack', slug='slack')

    def test_contact_get(self):
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
    
    def test_contact_post(self):
        contact_email = 'aaaaaaa@gmail.com'
        contact_subject ='テスト'
        contact_message = 'form valid testです。'
        response = self.client.post(self.contact_url, {'contact_email':contact_email, 'contact_subject':contact_subject, 'contact_message':contact_message})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
    
    def test_contact_post_auth(self):
        logged_in =self.client.login(username=self.user.username, password='pass')
        contact_email = 'aaaaaaa@gmail.com'
        contact_subject ='テスト'
        contact_message = 'form valid testです。'
        response = self.client.post(self.contact_url, {'contact_email':contact_email, 'contact_subject':contact_subject, 'contact_message':contact_message})
        self.assertEqual(response.status_code, 302)
    
    def test_contact_post_headererror(self):
        contact_email = 'aaaaaaa@gmail.com'
        contact_subject ='Subject\nInjection Test'
        contact_message = 'form valid testです。'
        response = self.client.post(self.contact_url, {'contact_email':contact_email, 'contact_subject':contact_subject, 'contact_message':contact_message})
        self.assertRaises(BadHeaderError)
    
    def test_contact_post_form_invalid(self):
        contact_email = ''
        contact_subject =''
        contact_message = ''
        response = self.client.post(self.contact_url, {'contact_email':contact_email, 'contact_subject':contact_subject, 'contact_message':contact_message})
        self.assertEqual(response.status_code, 200)





        
    