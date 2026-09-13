from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from tag.models import Tag

from .models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin): ...


class TagInline(GenericStackedInline):
    model = Tag
    fields = ("name",)
    extra = 1


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
    inlines = [  # noqa: RUF012
        TagInline,
    ]


admin.site.register(Category, CategoryAdmin)
