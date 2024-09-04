import os
import tempfile
from behave import fixture, use_fixture

from app import create_app
from app.db import init_db

@fixture
def app_client(context, *args, **kwargs):
    context.db, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })
    context.client = app.test_client()
    with app.app_context():
        init_db()
    yield context.client
    # -- CLEANUP:
    os.close(context.db)
    os.unlink(db_path)

def before_feature(context, feature):
    # -- HINT: Recreate a new flaskr client before each feature is executed.
    use_fixture(app_client, context)