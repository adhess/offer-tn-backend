import pytest
import mimesis_factory
import factory
from mimesis import Person


def get_account_factory(username_field=None, email_field=None):
    class AccountFactory(factory.StubFactory):
        username = username_field
        email = email_field
        id = username

    return AccountFactory


def test_filling_attributes_with_factory_boy_declarations_returns_different_values_for_instances():
    account_factory = get_account_factory(username_field=mimesis_factory.MimesisField("username"))
    account = account_factory()
    assert account.username is not None
    account2 = account_factory()
    assert account2.username != account.username


def test_filling_attributes_with_custom_functions_always_returns_same_value():
    account_factory = get_account_factory(username_field=Person().username())
    account = account_factory()
    assert account.username is not None
    account2 = account_factory()
    assert account2.username == account.username


def test_filling_attributes_with_lazy_function_and_custom_functions_behaves_like_factory_declarations():
    get_username_func = Person().username
    account_factory = get_account_factory(username_field=factory.LazyFunction(get_username_func))

    account = account_factory()
    assert account.username is not None
    account2 = account_factory()
    assert account2.username != account.username


def test_using_self_attribute_instead_of_lazy_attribute_fails():
    account_factory = get_account_factory(username_field="Mohamed",
                                          email_field=f'{factory.SelfAttribute("username")}@gmail.com')
    account = account_factory()
    with pytest.raises(AssertionError):
        assert account.email == "Mohamed@gmail.com"
    assert account.email == str(factory.SelfAttribute("username")) + "@gmail.com"


def test_attribute_that_is_assigned_another_attribute_without_self_attribute_is_still_static():
    account_factory = get_account_factory(username_field="Mohamed")

    account = account_factory()
    assert account.id == "Mohamed"

    with pytest.raises(AssertionError):
        account = account_factory(username="thotslayer69")
        assert account.id == "thotslayer69"

