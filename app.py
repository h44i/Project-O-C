from flask import Flask, render_template, jsonify
from models import db, Status, Step

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/health")
def health():
    return jsonify(status="ok")


@app.route("/api/steps")
def steps():
    items = Step.query.order_by(Step.order_num).all()
    return jsonify([
        {"id": s.id, "title": s.title, "order": s.order_num, "deadline_days": s.deadline_days}
        for s in items
    ])


@app.cli.command("seed")
def seed():
    """Заполнить базу начальными данными."""
    if Status.query.first():
        print("База уже заполнена")
        return

    for entity in ("step", "application"):
        db.session.add_all([
            Status(code="new", name="Новый", entity=entity),
            Status(code="in_progress", name="В процессе", entity=entity),
            Status(code="done", name="Готово", entity=entity),
        ])

    db.session.add_all([
        Step(title="Миграционный учёт", order_num=1, deadline_days=7),
        Step(title="Медицинская страховка", order_num=2, deadline_days=14),
        Step(title="Банковская карта", order_num=3, deadline_days=30),
    ])
    db.session.commit()
    print("Готово")


if __name__ == "__main__":
    app.run(debug=True)
