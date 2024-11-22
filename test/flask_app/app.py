# flask_app/app.py
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'  # Используем SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель для записи
class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10000), nullable=False)

    def __repr__(self):
        return f"<Record {self.name}>"

# Создание базы данных
with app.app_context():
    db.create_all()

@app.route('/write', methods=['POST'])
def write():
    start_time = time.time()

    # Добавляем 100 записей в базу данных
    for i in range(100):
        record = Record(name=f"Record {i + 1}")
        db.session.add(record)
    db.session.commit()  # Подтверждаем транзакцию

    end_time = time.time()
    return jsonify({"message": f"Flask write of 100 records took {end_time - start_time} seconds"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
