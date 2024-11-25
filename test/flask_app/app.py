from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import time

app = Flask(__name__)

# Configuring the database URI for SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializing SQLAlchemy
db = SQLAlchemy(app)

# Model for a record
class Record(db.Model):
    """
    Represents a record in the database.

    Attributes:
        id (int): The primary key of the record.
        name (str): The name of the record.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10000), nullable=False)

    def __repr__(self):
        return f"<Record {self.name}>"

# Creating the database tables
with app.app_context():
    db.create_all()

@app.route('/write', methods=['POST'])
def write():
    """
    Inserts 100 records into the database.

    Measures the time taken to insert the records and returns it as a JSON response.

    Returns:
        dict: A message containing the time taken to write records.
    """
    start_time = time.time()  # Start timing the operation

    # Add 100 records to the database
    for i in range(100):
        record = Record(name=f"Record {i + 1}")
        db.session.add(record)

    db.session.commit()  # Commit the transaction

    end_time = time.time()  # End timing the operation

    # Return the time taken for the operation
    return jsonify({"message": f"Flask write of 100 records took {end_time - start_time:.2f} seconds"})

if __name__ == '__main__':
    # Run the Flask application in debug mode on port 5000
    app.run(debug=True, port=5000)
