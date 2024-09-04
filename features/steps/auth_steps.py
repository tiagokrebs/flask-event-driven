from behave import given, when, then
from tests.conftest import AuthActions

@given('I am a user with username "{username}" and password "{password}"')
def step_given_user(context, username, password):
    context.username = username
    context.password = password

@when('I login')
def step_when_login(context):
    auth = AuthActions(context.client)
    response = auth.login(username=context.username, password=context.password)
    context.response = response

@then('I should see a success message')
def step_then_success(context):
    auth = AuthActions(context.client)
    response = auth.login(username=context.username, password=context.password)
    print(response.data)
    assert response.status_code == 200
    assert b"Login successful" in response.data

@then('I should see an error message')
def step_then_error(context):
    auth = AuthActions(context.client)
    response = auth.login(username=context.username, password=context.password)
    print(response.data)
    # assert response.status_code == 200
    assert b"Incorrect username" in response.data