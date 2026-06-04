"""Testes para os views de receitas"""

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    """Testes para os views de receitas"""

    def test_recipe_home_view_function_is_correct(self):
        """Teste para verificar se a função da view home é a correta"""
        view = resolve(reverse("recipes:home"))
        self.assertIs(view.func, views.home)

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

    def test_recipe_category_view_function_is_correct(self):
        """Teste para verificar se a função da view de categoria é a correta"""
        view = resolve(reverse("recipes:category", kwargs={"category_id": 1000}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        """Teste para verificar se a view de categoria retorna o status code
        404 quando não há receitas"""
        response = self.client.get(
            reverse("recipes:category", kwargs={"category_id": 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        """Teste para verificar se o template da view de categoria carrega as
        receitas"""

        needed_title = "This is a category test"
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse("recipes:category", args=(1,)))
        content = response.content.decode("utf-8")
        self.assertIn(needed_title, content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Teste para verificar se quando o published for False a receita
        não é carregada no template da view category"""

        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse(
                "recipes:recipe",
                kwargs={
                    "id": recipe.category.id,
                },
            )
        )

        self.assertEqual(response.status_code, 404)

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

    def test_recipe_search_view_function_is_correct(self):
        """Teste para verificar se a função da view search é a correta"""
        view = resolve(reverse("recipes:search"))
        self.assertIs(view.func, views.search)

    def test_recipe_search_view_loads_correct_template(self):
        """Teste para verificar se a view search carrega o template correto"""
        response = self.client.get(reverse("recipes:search"))
        self.assertTemplateUsed(response, "recipes/pages/search.html")

    def test_recipe_search_raises_404_if_no_search_term(self):
        """Teste para verificar se a view search retorna o status code 404
        quando não há termo de busca"""
        url = reverse("recipes:search")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
