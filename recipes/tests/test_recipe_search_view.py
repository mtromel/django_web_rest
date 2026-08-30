"""Testes para os views de receitas"""

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    """Testes para os views de receitas"""

    def test_recipe_search_view_function_is_correct(self):
        """Teste para verificar se a função da view search é a correta"""
        view = resolve(reverse("recipes:search"))
        self.assertIs(view.func.view_class, views.RecipeListViewSearch)

    def test_recipe_search_view_loads_correct_template(self):
        """Teste para verificar se a view search carrega o template correto"""
        response = self.client.get(reverse("recipes:search") + "?q=teste")
        self.assertTemplateUsed(response, "recipes/pages/search.html")

    def test_recipe_search_raises_404_if_no_search_term(self):
        """Teste para verificar se a view search retorna o status code 404
        quando não há termo de busca"""
        url = reverse("recipes:search")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        """Teste para verificar se o termo de busca está no título da página e
        escapado"""
        url = reverse("recipes:search") + "?q=<teste>"
        response = self.client.get(url)
        self.assertIn(
            "Search for &quot;&lt;teste&gt;&quot; |", response.content.decode("utf-8")
        )

    def test_recipe_search_can_find_recipe_by_title(self):
        """Teste para verificar se a view search pode encontrar receitas pelo título"""
        title1 = "This is recipe one"
        title2 = "This is recipe two"
        recipe1 = self.make_recipe(
            slug="one", title=title1, author_data={"username": "one"}
        )
        recipe2 = self.make_recipe(
            slug="two", title=title2, author_data={"username": "two"}
        )

        search_url = reverse("recipes:search")
        response1 = self.client.get(f"{search_url}?q={title1}")
        response2 = self.client.get(f"{search_url}?q={title2}")
        response_both = self.client.get(f"{search_url}?q=this")

        self.assertIn(recipe1, response1.context["recipes"])
        self.assertNotIn(recipe2, response1.context["recipes"])

        self.assertIn(recipe2, response2.context["recipes"])
        self.assertNotIn(recipe1, response2.context["recipes"])

        self.assertIn(recipe1, response_both.context["recipes"])
        self.assertIn(recipe2, response_both.context["recipes"])
