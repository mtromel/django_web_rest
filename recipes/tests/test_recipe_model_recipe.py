from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def test_recipe_title_raises_error_if_title_has_more_than_65_characters(self):
        """Teste para verificar se o título da receita lança um erro quando
        tem mais de 65 caracteres"""
        self.recipe.title = "A" * 70
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    @parameterized.expand(
        [
            ("title", 65),
            ("description", 165),
            ("preparation_time_unit", 65),
            ("servings_unit", 65),
        ]
    )
    def test_recipe_fields_max_length(self, field, max_length):
        """Teste para verificar se os campos da receita tem o max_length correto"""
        setattr(self.recipe, field, "A" * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
