import os

from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash

from src import create_app, db
from src.models import User, Document


app = create_app()
cli = FlaskGroup(create_app=create_app)
DEFAULT_PASSWORD = os.getenv("DEFAULT_PASSWORD", "123456")


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    user_1 = User(
        username="jsanchez",
        password=generate_password_hash(DEFAULT_PASSWORD),
        first_name="Juan",
        last_name="Sanchez",
    )
    user_2 = User(
        username="jperez",
        password=generate_password_hash(DEFAULT_PASSWORD),
        first_name="Juan",
        last_name="Perez",
    )
    db.session.add(user_1)
    db.session.add(user_2)
    db.session.commit()
    document_1 = Document(
        document_name="sample.pdf",
        url="https://uanataca.pythonanywhere.com/sample.pdf",
        user_id=user_1.id,
    )
    document_2 = Document(
        document_name="dummy.pdf",
        url="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
        user_id=user_1.id,
    )
    document_3 = Document(
        document_name="Test_PDF.pdf",
        url="https://www.gemini.com/documents/credit/Test_PDF.pdf",
        user_id=user_1.id,
    )
    document_4 = Document(
        document_name="test.pdf",
        url="http://s29.q4cdn.com/175625835/files/doc_downloads/test.pdf",
        user_id=user_2.id,
    )
    document_5 = Document(
        document_name="TestPDFfile.pdf",
        url="https://www.clickdimensions.com/links/TestPDFfile.pdf",
        user_id=user_2.id,
    )
    db.session.add(document_1)
    db.session.add(document_2)
    db.session.add(document_3)
    db.session.add(document_4)
    db.session.add(document_5)
    db.session.commit()
    

if __name__ == "__main__":
    cli()
