from django.test import TestCase
from blogs.forms import ContactForm
from blogs.models import Category, PostModel

# Create your tests here
class ContactFormTestCase(TestCase):

    def test_valid_form(self):
        contact_email = 'aaaaaaa@gmail.com'
        contact_subject ='テスト'
        contact_message = 'form valid testです。'
        data = {'contact_email':contact_email, 'contact_subject':contact_subject, 'contact_message':contact_message}
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form(self):
        contact_email = 'aaaaaaa@gmail.com'
        contact_subject ='テスト'
        contact_message = ''
        data = {'contact_email':contact_email, 'contact_subject':contact_subject, 'contact_message':contact_message}
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
