from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'  # Using SQLite for demonstration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(80), nullable=False)
    asset_description = db.Column(db.String(200))
    manufacturer = db.Column(db.String(80))
    # ... You can add other fields as needed ...

    def serialize(self):
        return {
            "id": self.id,
            "asset_name": self.asset_name,
            "asset_description": self.asset_description,
            "manufacturer": self.manufacturer,
            # ... serialize other fields similarly ...
        }


@app.route('/assets', methods=['POST'])
def create_asset():
    data = request.get_json()
    new_asset = Asset(**data)
    db.session.add(new_asset)
    db.session.commit()
    return jsonify({"message": "Asset created", "asset": new_asset.serialize()}), 201


@app.route('/assets', methods=['GET'])
def get_assets():
    assets = Asset.query.all()
    return jsonify([asset.serialize() for asset in assets])


@app.route('/assets/<int:id>', methods=['GET'])
def get_asset(id):
    asset = Asset.query.get_or_404(id)
    return jsonify(asset.serialize())


@app.route('/assets/<int:id>', methods=['PUT'])
def update_asset(id):
    asset = Asset.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(asset, key, value)
    db.session.commit()
    return jsonify({"message": "Asset updated", "asset": asset.serialize()})


@app.route('/assets/<int:id>', methods=['DELETE'])
def delete_asset(id):
    asset = Asset.query.get_or_404(id)
    db.session.delete(asset)
    db.session.commit()
    return jsonify({"message": "Asset deleted"})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates the tables in the database
    app.run(debug=True)

