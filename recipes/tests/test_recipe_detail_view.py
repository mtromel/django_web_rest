"""Testes para os views de receitas"""

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    """Testes para os views de receitas"""

    def test_recipe_detail_view_function_is_correct(self):
        """Teste para verificar se a função da view de detalhe é a correta"""
        view = resolve(reverse("recipes:recipe", kwargs={"id": 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        """Teste para verificar se a view de detalhe retorna o status code
        404 quando não há receitas"""
        response = self.client.get(reverse("recipes:recipe", kwargs={"id": 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        """Teste para verificar se o template da view de detalhe carrega a
        receita correta"""

        needed_title = "This is a detail page - It load one recipe"
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse("recipes:recipe", kwargs={"id": 1}))
        content = response.content.decode("utf-8")
        self.assertIn(needed_title, content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        """Teste para verificar se quando o published for False a receita
        não é carregada no template da view category"""

        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse(
                "recipes:recipe",
                kwargs={
                    "id": recipe.id,
                },
            )
        )

        self.assertEqual(response.status_code, 404)
