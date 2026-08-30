"""Testes para os views de receitas"""

from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
    """Testes para os views de receitas"""

    def test_recipe_home_view_function_is_correct(self):
        """Teste para verificar se a função da view home é a correta"""
        view = resolve(reverse("recipes:home"))
        self.assertIs(view.func.view_class, views.RecipeListViewHome)

    def test_recipe_home_view_returns_status_code_200(self):
        """Teste para verificar se a view home retorna o status code 200"""
        response = self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        """Teste para verificar se a view home carrega o template correto"""
        response = self.client.get(reverse("recipes:home"))
        self.assertTemplateUsed(response, "recipes/pages/home.html")

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        """Teste para verificar se o template da view home mostra mensagem de
        nenhuma receita encontrada quando não há receitas"""
        response = self.client.get(reverse("recipes:home"))
        self.assertIn(
            "<h1> No recipes found here... 😒 </h1>", response.content.decode("utf-8")
        )

    def test_recipe_home_template_loads_recipes(self):
        """Teste para verificar se o template da view home carrega as
        receitas"""

        self.make_recipe()
        response = self.client.get(reverse("recipes:home"))
        content = response.content.decode("utf-8")
        response_context_recipes = response.context["recipes"]
        self.assertIn("Recipe Title", content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Teste para verificar se quando o published for False a receita
        não é carregada no template da view home"""

        self.make_recipe(is_published=False)
        response = self.client.get(reverse("recipes:home"))

        self.assertIn(
            "<h1> No recipes found here... 😒 </h1>", response.content.decode("utf-8")
        )

    def test_recipe_home_is_paginated(self):

        self.make_recipe_in_batch(qtd=8)

        with patch("recipes.views.PER_PAGE", new=3):
            response = self.client.get(reverse("recipes:home"))
            recipess = response.context["recipes"]
            paginator = recipess.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)

    def test_invalid_page_query_uses_page_one(self):
        self.make_recipe_in_batch(qtd=8)

        with patch("recipes.views.PER_PAGE", new=3):
            response = self.client.get(reverse("recipes:home") + "?page=1A")
            self.assertEqual(response.context["recipes"].number, 1)

            response = self.client.get(reverse("recipes:home") + "?page=2")
            self.assertEqual(response.context["recipes"].number, 2)

            response = self.client.get(reverse("recipes:home") + "?page=3")
            self.assertEqual(response.context["recipes"].number, 3)
