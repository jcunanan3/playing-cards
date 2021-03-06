from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from utils import create_deck
from models import Card, Player
# from models import get_war_result
from forms import EmailUserCreationForm
from test_utils import run_pyflakes_for_package, run_pep8_for_package

__author__ = 'joaquincunanan'

from django.test import TestCase
class BasicMathTestCase(TestCase):
    def test_math(self):
        a = 1
        b = 1
        self.assertEqual(a+b, 2)

    # def test_failing_case(self):
    #     a = 1
    #     b = 1
    #     self.assertEqual(a+b, 1)

class UtilTestCase(TestCase):
    def test_create_deck_count(self):
        """Test that we created 52 cards"""
        create_deck()
        self.assertEqual(Card.objects.count(), 52)


class ModelTestCase(TestCase):
    def test_get_ranking(self):
        """Test that we get the proper ranking for a card"""
        card = Card.objects.create(suit=Card.CLUB, rank="jack")
        self.assertEqual(card.get_ranking(), 11)



class FormTestCase(TestCase):
    def test_clean_username_exception(self):
        # Create a player so that this username we're testing is already taken
        Player.objects.create_user(username='test-user')

        # set up the form for testing
        form = EmailUserCreationForm()
        form.cleaned_data = {'username': 'test-user'}

        # use a context manager to watch for the validation error being raised
        with self.assertRaises(ValidationError):
            form.clean_username()


    # def test_clean_username_ok(self):
    #     # Create a player so that this username we're testing is already taken
    #     Player.objects.create_user(username='test-user')
    #
    #     # use a context manager to watch for the validation error being raised
    #     self.assertEquals(form.clean_username(),'test-user')
    #


class ViewTestCase(TestCase):
    def setUp(self):
        create_deck()

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertIn('<p>Suit: spade, Rank: two</p>', response.content)
        self.assertEqual(response.context['cards'].count(), 52)


    def test_FAQ(self):
        response = self.client.get(reverse('faq'))
        # Check it's a redirect to the profile page
        self.assertIn('<p>Q: Can I win real money on this website?</p>', response.content)
        self.assertIsInstance(response, HttpResponse)
        # self.assertTrue(response.get('location').endswith(reverse('faq')))

class SyntaxTest(TestCase):
    def test_syntax(self):
        """
        Run pyflakes/pep8 across the code base to check for potential errors.
        """
        packages = ['cards']
        warnings = []
        # Eventually should use flake8 instead so we can ignore specific lines via a comment
        for package in packages:
            warnings.extend(run_pyflakes_for_package(package, extra_ignore=("_settings",)))
            warnings.extend(run_pep8_for_package(package, extra_ignore=("_settings",)))
        if warnings:
            self.fail("{0} Syntax warnings!\n\n{1}".format(len(warnings), "\n".join(warnings)))

def test_profile(self):
        response = self.client.get(reverse('profile'))
        # Check it's a redirect to the profile page
        self.assertIn("<p>Hi {{ user.username }}, you have {{wins}} wins and {{losses}} losses.</p>", response.content)
        self.assertIsInstance(response, HttpResponse)