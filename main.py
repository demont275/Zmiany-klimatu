# Importowanie
from flask import Flask, redirect, render_template, request, url_for
# Podlaczanie biblioteki do baz danych
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Nawiazanie polaczenia SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///feedback.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Tworzenie BD
db = SQLAlchemy(app)


# Tworzenie tabeli
class Feedback(db.Model):
    # Ustanowienie pol wejsciowych
    # id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Tytul
    title = db.Column(db.String(100), nullable=False)
    # Podtytul
    subtitle = db.Column(db.String(300), nullable=False)
    # Tekst
    text = db.Column(db.Text, nullable=False)
    # Adres e-mail autora feedbacku
    user_email = db.Column(db.String(100), nullable=False)

    # Wyswietlanie obiektu i jego identyfikatora
    def __repr__(self):
        return f"<Feedback {self.id}>"


# Tworzenie tabel po uruchomieniu
with app.app_context():
    db.create_all()


# Uruchamianie strony z trescia
@app.route("/")
def index():
    feedbacks = Feedback.query.order_by(Feedback.id.desc()).all()
    return render_template("index.html", feedbacks=feedbacks)


# Formularz feedbacku
@app.route("/feedback", methods=["POST"])
def save_feedback():
    email = request.form.get("email", "").strip()
    text = request.form.get("text", "").strip()

    if not email or not text:
        return redirect(url_for("index"))

    feedback = Feedback(
        title=f"Feedback od {email}",
        subtitle="Pomysl na ograniczenie zmian klimatu",
        text=text,
        user_email=email,
    )
    db.session.add(feedback)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
