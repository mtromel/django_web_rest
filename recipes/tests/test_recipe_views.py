'''Testes para os views de receitas'''

from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views
from recipes.models import Category, Recipe, User


class RecipeViewsTest(TestCase):
    '''Testes para os views de receitas'''

    def test_recipe_home_view_function_is_correct(self):
        '''Teste para verificar se a função da view home é a correta'''
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200(self):
        '''Teste para verificar se a view home retorna o status code 200'''
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        '''Teste para verificar se a view home carrega o template correto'''
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        '''Teste para verificar se o template da view home mostra mensagem de
        nenhuma receita encontrada quando não há receitas'''
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('<h1> No recipes found here... 😒 </h1>',
                      response.content.decode('utf-8')
                      )

    def test_recipe_home_template_loads_recipes(self):
        '''Teste para verificar se o template da view home carrega as
        receitas'''
        category = Category.objects.create(name='Category')
        author = User.objects.create_user(
            first_name='user',
            last_name='name',
            username='username',
            password='123456',
            email='username@email.com'
        )
        recipe = Recipe.objects.create(
            category=category,
            author=author,
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
            preparation_steps_is_html=False,
            is_published=True,
        )
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        self.assertIn('Recipe Title', content)
        self.assertIn('10 Minutos', content)
        self.assertIn('5 Porções', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_category_view_function_is_correct(self):
        '''Teste para verificar se a função da view de categoria é a correta'''
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        '''Teste para verificar se a view de categoria retorna o status code
        404 quando não há receitas'''
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_function_is_correct(self):
        '''Teste para verificar se a função da view de detalhe é a correta'''
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        '''Teste para verificar se a view de detalhe retorna o status code
        404 quando não há receitas'''
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)
