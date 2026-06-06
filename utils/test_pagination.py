from unittest import TestCase

from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        """Teste para verificar se a função make_pagination_range retorna um range de paginação"""

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )["pagination"]
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):
        """Teste para verificar se a primeira range é estática se a página atual for menor que a página do meio"""

        # current_page = 1 - qty_pages = 4 - middle_page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )["pagination"]
        self.assertEqual([1, 2, 3, 4], pagination)

        # current_page = 2 - qty_pages = 4 - middle_page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2,
        )["pagination"]
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_make_sure_middle_ranges_are_correct(self):
        """Teste para verificar se o range muda se a página atual for maior que a página do meio"""

        # current_page = 10 - qty_pages = 4 - middle_page = 2
        # Here range should change
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=10,
        )["pagination"]
        self.assertEqual([9, 10, 11, 12], pagination)

        # current_page = 12 - qty_pages = 4 - middle_page = 2
        # Here range should change
        pagination = make_pagination_range(
            page_range=list(range(1, 21)), qty_pages=4, current_page=12
        )["pagination"]
        self.assertEqual([11, 12, 13, 14], pagination)

    def test_make_pagination_range_is_static_when_last_page_is_next(self):
        """Teste para verificar se o range é estático quando a última página é a próxima"""

        # current_page = 18 - qty_pages = 4 - middle_page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=18,
        )["pagination"]
        self.assertEqual([17, 18, 19, 20], pagination)

        # current_page = 19 - qty_pages = 4 - middle_page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19,
        )["pagination"]
        self.assertEqual([17, 18, 19, 20], pagination)

        # current_page = 20 - qty_pages = 4 - middle_page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20,
        )["pagination"]
        self.assertEqual([17, 18, 19, 20], pagination)

        # current_page = 21 - qty_pages = 4 - middle_page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=21,
        )["pagination"]
        self.assertEqual([17, 18, 19, 20], pagination)
