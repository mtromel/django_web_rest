from django.contrib import admin

from .models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin): ...


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [  # noqa: RUF012
        "id",
        "title",
        "created_at",
        "is_published",
        "author",
    ]
    list_display_links = [  # noqa: RUF012
        "title",
        "created_at",
    ]
    search_fields = [  # noqa: RUF012
        "id",
        "title",
        "description",
        "slug",
        "preparation_steps",
    ]
    list_filter = [  # noqa: RUF012
        "category",
        "author",
        "is_published",
        "preparation_steps_is_html",
    ]
    list_per_page = 10
    list_editable = [  # noqa: RUF012
        "is_published",
    ]
    ordering = ["-id"]  # noqa: RUF012
    prepopulated_fields = {  # noqa: RUF012
        "slug": ("title",)
    }


admin.site.register(Category, CategoryAdmin)
