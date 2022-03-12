import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_category_view_set(api_client, create_category):
    electronics = create_category(name='Electronics')
    computer = create_category(name='Computers', parent=electronics)
    phone = create_category(name='Phones', parent=electronics)
    laptop = create_category(name='laptop', parent=computer)

    url = reverse("categories-list")
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data == {
        'count': 1,
        'next': None,
        'previous': None,
        'results': [
            {
                'id': electronics.pk,
                'name': electronics.name,
                'children': [
                    {
                        'id': computer.pk,
                        'name': computer.name,
                        'children': [
                            {
                                'id': laptop.pk,
                                'name': laptop.name,
                                'children': [],
                                'icon': '',
                                'isActive': False
                            }
                        ],
                        'icon': '',
                        'isActive': False

                    },
                    {
                        'id': phone.pk,
                        'name': phone.name,
                        'children': [],
                        'icon': '',
                        'isActive': False
                    }
                ],
                'icon': "",
                'isActive': False,

            }
        ]

    }
