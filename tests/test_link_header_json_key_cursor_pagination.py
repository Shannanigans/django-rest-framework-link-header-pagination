# coding: utf-8
from __future__ import unicode_literals

from django.test import override_settings
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

import drf_link_header_pagination

from .test_link_header_cursor_pagination import TestLinkHeaderCursorPagination
from .mocks import MockObject, MockQuerySet

factory = APIRequestFactory()


class TestLinkHeaderJsonKeyCursorPagination(TestLinkHeaderCursorPagination):
    """
    Unit tests for `pagination.LinkHeaderJsonKeyCursorPagination`.
    """

    def setup(self):
        class ExamplePagination(
            drf_link_header_pagination.LinkHeaderJsonKeyCursorPagination
        ):
            page_size = 5
            page_size_query_param = "page_size"
            max_page_size = 20
            ordering = "created"

        self.pagination = ExamplePagination()
        self.queryset = MockQuerySet(
            [
                MockObject(idx)
                for idx in [
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    2,
                    3,
                    4,
                    4,
                    4,
                    4,
                    5,
                    6,
                    7,
                    7,
                    7,
                    7,
                    7,
                    7,
                    7,
                    7,
                    7,
                    8,
                    9,
                    9,
                    9,
                    9,
                    9,
                    9,
                ]
            ]
        )

    @override_settings(ALLOWED_HOSTS=["testserver"])
    def test_no_cursor(self):
        url = "/"
        request = Request(factory.get(url))
        queryset = self.paginate_queryset(request)
        response = self.get_paginated_response(queryset)
        response_next_url = response.data["next"]
        response_previous_url = response.data["previous"]
        (_, _, _, previous_url, next_url) = self.get_pages(url)
        assert response_next_url == next_url
        assert response_previous_url == previous_url
        response_data_values = [item.value for item in response.data["results"]]
        assert response_data_values == [1, 1, 1, 1, 1]

    @override_settings(ALLOWED_HOSTS=["testserver"])
    def test_second_page(self):
        first_page_url = "/"
        (_, _, _, _, second_page_url) = self.get_pages(first_page_url)

        request = Request(factory.get(second_page_url))
        queryset = self.paginate_queryset(request)
        response = self.get_paginated_response(queryset)
        response_next_url = response.data["next"]
        response_previous_url = response.data["previous"]
        (_, _, _, previous_url, next_url) = self.get_pages(second_page_url)
        assert response_next_url == next_url
        assert response_previous_url == previous_url
        response_data_values = [item.value for item in response.data["results"]]
        assert response_data_values == [1, 2, 3, 4, 4]