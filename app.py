from flask import Flask, make_response, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt, decode_token
from flask_wtf.csrf import generate_csrf
from flask_cors import CORS
from datetime import datetime




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'  # Using SQLite for testing
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '57fb8e0169261ee55a08669d184976ae8d914c32f012bd0d' 
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
app.secret_key = "cda50149471a557db65e6e604fe7147e7e92a4f32657d164086697eb555d5d55"

CORS(app, resources={
    r"/*": {
        "origins": ["https://inv.goldenedit.dev"],
        "allow_headers": ["Content-Type", "Authorization", "X-CSRFToken"],
    }
})




bcrypt = Bcrypt(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)
    allocation_id = db.Column(db.Integer, db.ForeignKey('allocations.id'), nullable=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    home_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    barcode = db.Column(db.String(80))
    picture = db.Column(db.String(200))
    rfid = db.Column(db.String(80))
    qr_code = db.Column(db.String(80))
    asset_name = db.Column(db.String(80), nullable=False)
    asset_serial = db.Column(db.String(80))
    model_id = db.Column(db.Integer)
    asset_description = db.Column(db.String(200))
    manufacturer = db.Column(db.String(80))
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    disposal_date = db.Column(db.DateTime)
    disposal_reason = db.Column(db.String(200))
    disposal_type_id = db.Column(db.Integer, db.ForeignKey('disposal_type.id'))
    colour = db.Column(db.String(50))
    estimated_value = db.Column(db.Float)
    purchase_supplier = db.Column(db.String(80))
    date_purchased = db.Column(db.DateTime)
    warranty_details = db.Column(db.String(200))
    high_value = db.Column(db.Boolean, default=False)
    cannot_lend = db.Column(db.Boolean, default=False)
    asset_owner = db.Column(db.Integer, db.ForeignKey('people.id'))
    asset_type_id = db.Column(db.Integer, db.ForeignKey('asset_type.id'))

        # TODO Asset serialization code needed
    def serialize(self):
        return{
             "id": self.id,
            "group_id": self.group_id,
            "allocation_id": self.allocation_id,
            "location_id": self.location_id,
            "home_id": self.home_id,
            "barcode": self.barcode,
            "picture": self.picture,
            "rfid": self.rfid,
            "qr_code": self.qr_code,
            "asset_name": self.asset_name,
            "asset_serial": self.asset_serial,
            "model_id": self.model_id,
            "asset_description": self.asset_description,
            "manufacturer": self.manufacturer,
            "purchase_date": self.purchase_date.isoformat(),
            "disposal_date": self.disposal_date.isoformat(),
            "disposal_reason": self.disposal_reason,
            "disposal_type_id": self.disposal_type_id,
            "colour": self.colour,
            "estimated_value": self.estimated_value,
            "purchase_supplier": self.purchase_supplier,
            "date_purchased": self.date_purchased.isoformat(),
            "warranty_details": self.warranty_details,
            "high_value": self.high_value,
            "cannot_lend": self.cannot_lend,
            "asset_owner": self.asset_owner,
            "asset_type_id": self.asset_type_id
        }

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(80), nullable=False)
    group_description = db.Column(db.String(200))

    def serialize(self):
        return {
            "id": self.id,
            "group_name": self.group_name,
            "group_description": self.group_description
        }

class DisposalType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disposal_name = db.Column(db.String(80), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "disposal_name": self.disposal_name
        }

class AssetType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(80), nullable=False)
    type_description = db.Column(db.String(200))

    def serialize(self):
        return {
            "id": self.id,
            "type_name": self.type_name,
            "type_description": self.type_description
        }

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(80), nullable=False)
    location_area = db.Column(db.String(80))

    def serialize(self):
        return {
            "id": self.id,
            "location_name": self.location_name,
            "location_area": self.location_area
        }

class Allocations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    return_due_date = db.Column(db.DateTime)
    returned_date = db.Column(db.DateTime)

    def serialize(self):
        return {
            "id": self.id,
            "person_id": self.person_id,
            "timestamp": self.timestamp,
            "return_due_date": self.return_due_date.isoformat(),
            "returned_date": self.returned_date.isoformat(),
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_name = db.Column(db.String(80), nullable=False)
    person_department = db.Column(db.String(80))
    school = db.Column(db.String(80))
    lend = db.Column(db.Boolean, default=True)
    staff = db.Column(db.Boolean, default=False)
    rfid = db.Column(db.String(80))
    barcode = db.Column(db.String(80))
    can_log_in = db.Column(db.Boolean, default=True)
    email = db.Column(db.String(100))
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def serialize(self):
        return {
            "id": self.id,
            "person_name": self.person_name,
            "person_department": self.person_department,
            "school": self.school,
            "lend": self.lend,
            "staff": self.staff,
            "rfid": self.rfid,
            "barcode": self.barcode,
            "can_log_in": self.can_log_in,
            "email": self.email
        }

class GroupItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    item_name = db.Column(db.String(80), nullable=False)
    item_description = db.Column(db.String(200))

    def serialize(self):
        return {
            "id": self.id,
            "group_id": self.group_id,
            "item_name": self.item_name,
            "item_description": self.item_description
        }

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # TODO Fields for Role

    def serialize(self):
        return {
            "id": self.id
            # Add other fields once they're defined
        }




# >>>>>> API Routes <<<<<<

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response


# ASSET

# Create Asset
@app.route('/assets', methods=['POST'])
@jwt_required()
def create_asset():
    data = request.get_json()
    try:
        new_asset = Asset(**data)
        db.session.add(new_asset)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    return jsonify({"message": "Asset created", "asset": new_asset.serialize()}), 201

# Get All Assets
@app.route('/assets', methods=['GET'])
@jwt_required()
def get_assets():
    assets = Asset.query.all()
    return jsonify([asset.serialize() for asset in assets])

# Get Single Asset by ID
@app.route('/assets/<int:id>', methods=['GET'])
@jwt_required()
def get_asset(id):
    asset = Asset.query.get_or_404(id)
    return jsonify(asset.serialize())

# Update Asset by ID
@app.route('/assets/<int:id>', methods=['PUT'])
@jwt_required()
def update_asset(id):
    asset = Asset.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(asset, key, value)
    db.session.commit()
    return jsonify({"message": "Asset updated", "asset": asset.serialize()})

# Delete Asset by ID
@app.route('/assets/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_asset(id):
    asset = Asset.query.get_or_404(id)
    db.session.delete(asset)
    db.session.commit()
    return jsonify({"message": "Asset deleted"})



# GROUPS

@app.route('/groups', methods=['POST'])
@jwt_required()
def create_group():
    data = request.get_json()
    new_group = Group(**data)
    db.session.add(new_group)
    db.session.commit()
    return jsonify({"message": "Group created", "group": new_group.serialize()}), 201

@app.route('/groups', methods=['GET'])
@jwt_required()
def get_groups():
    groups = Group.query.all()
    return jsonify([group.serialize() for group in groups])

@app.route('/groups/<int:id>', methods=['GET'])
@jwt_required()
def get_group(id):
    group = Group.query.get_or_404(id)
    return jsonify(group.serialize())

@app.route('/groups/<int:id>', methods=['PUT'])
@jwt_required()
def update_group(id):
    group = Group.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(group, key, value)
    db.session.commit()
    return jsonify({"message": "Group updated", "group": group.serialize()})

@app.route('/groups/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_group(id):
    group = Group.query.get_or_404(id)
    db.session.delete(group)
    db.session.commit()
    return jsonify({"message": "Group deleted"})


# DISPOSAL TYPES

@app.route('/disposal_types', methods=['POST'])
@jwt_required()
def create_disposal_type():
    data = request.get_json()
    new_disposal_type = DisposalType(**data)
    db.session.add(new_disposal_type)
    db.session.commit()
    return jsonify({"message": "Disposal type created", "disposal_type": new_disposal_type.serialize()}), 201

@app.route('/disposal_types', methods=['GET'])
@jwt_required()
def get_disposal_types():
    disposal_types = DisposalType.query.all()
    return jsonify([disposal_type.serialize() for disposal_type in disposal_types])

@app.route('/disposal_types/<int:id>', methods=['GET'])
@jwt_required()
def get_disposal_type(id):
    disposal_type = DisposalType.query.get_or_404(id)
    return jsonify(disposal_type.serialize())

@app.route('/disposal_types/<int:id>', methods=['PUT'])
@jwt_required()
def update_disposal_type(id):
    disposal_type = DisposalType.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(disposal_type, key, value)
    db.session.commit()
    return jsonify({"message": "Disposal type updated", "disposal_type": disposal_type.serialize()})

@app.route('/disposal_types/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_disposal_type(id):
    disposal_type = DisposalType.query.get_or_404(id)
    db.session.delete(disposal_type)
    db.session.commit()
    return jsonify({"message": "Disposal type deleted"})


# ASSET TYPES


@app.route('/asset_types', methods=['POST'])
@jwt_required()
def create_asset_type():
    data = request.get_json()
    new_asset_type = AssetType(**data)
    db.session.add(new_asset_type)
    db.session.commit()
    return jsonify({"message": "Asset type created", "asset_type": new_asset_type.serialize()}), 201

@app.route('/asset_types', methods=['GET'])
@jwt_required()
def get_asset_types():
    asset_types = AssetType.query.all()
    return jsonify([asset_type.serialize() for asset_type in asset_types])

@app.route('/asset_types/<int:id>', methods=['GET'])
@jwt_required()
def get_asset_type(id):
    asset_type = AssetType.query.get_or_404(id)
    return jsonify(asset_type.serialize())

@app.route('/asset_types/<int:id>', methods=['PUT'])
@jwt_required()
def update_asset_type(id):
    asset_type = AssetType.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(asset_type, key, value)
    db.session.commit()
    return jsonify({"message": "Asset type updated", "asset_type": asset_type.serialize()})

@app.route('/asset_types/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_asset_type(id):
    asset_type = AssetType.query.get_or_404(id)
    db.session.delete(asset_type)
    db.session.commit()
    return jsonify({"message": "Asset type deleted"})


# LOCATION

@app.route('/locations', methods=['POST'])
@jwt_required()
def create_location():
    data = request.get_json()
    new_location = Location(**data)
    db.session.add(new_location)
    db.session.commit()
    return jsonify({"message": "Location created", "location": new_location.serialize()}), 201

@app.route('/locations', methods=['GET'])
@jwt_required()
def get_locations():
    locations = Location.query.all()
    return jsonify([location.serialize() for location in locations])

@app.route('/locations/<int:id>', methods=['GET'])
@jwt_required()
def get_location(id):
    location = Location.query.get_or_404(id)
    return jsonify(location.serialize())

@app.route('/locations/<int:id>', methods=['PUT'])
@jwt_required()
def update_location(id):
    location = Location.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(location, key, value)
    db.session.commit()
    return jsonify({"message": "Location updated", "location": location.serialize()})

@app.route('/locations/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_location(id):
    location = Location.query.get_or_404(id)
    db.session.delete(location)
    db.session.commit()
    return jsonify({"message": "Location deleted"})


# ALLOCATIONS

@app.route('/allocations', methods=['POST'])
@jwt_required()
def create_allocation():
    data = request.get_json()
    new_allocation = Allocations(**data)
    db.session.add(new_allocation)
    db.session.commit()
    return jsonify({"message": "Allocation created", "allocation": new_allocation.serialize()}), 201

@app.route('/allocations', methods=['GET'])
@jwt_required()
def get_allocations():
    allocations = Allocations.query.all()
    return jsonify([allocation.serialize() for allocation in allocations])

@app.route('/allocations/<int:id>', methods=['GET'])
@jwt_required()
def get_allocation(id):
    allocation = Allocations.query.get_or_404(id)
    return jsonify(allocation.serialize())

@app.route('/allocations/<int:id>', methods=['PUT'])
@jwt_required()
def update_allocation(id):
    allocation = Allocations.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(allocation, key, value)
    db.session.commit()
    return jsonify({"message": "Allocation updated", "allocation": allocation.serialize()})

@app.route('/allocations/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_allocation(id):
    allocation = Allocations.query.get_or_404(id)
    db.session.delete(allocation)
    db.session.commit()
    return jsonify({"message": "Allocation deleted"})


# PEOPLE

@app.route('/people', methods=['POST'])
@jwt_required()
def create_person():
    data = request.get_json()
    new_person = People(**data)
    db.session.add(new_person)
    db.session.commit()
    return jsonify({"message": "Person created", "person": new_person.serialize()}), 201

@app.route('/people', methods=['GET'])
@jwt_required()
def get_people():
    people = People.query.all()
    return jsonify([person.serialize() for person in people])

@app.route('/people/<int:id>', methods=['GET'])
@jwt_required()
def get_person(id):
    person = People.query.get_or_404(id)
    return jsonify(person.serialize())

@app.route('/people/<int:id>', methods=['PUT'])
@jwt_required()
def update_person(id):
    person = People.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(person, key, value)
    db.session.commit()
    return jsonify({"message": "Person updated", "person": person.serialize()})

@app.route('/people/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_person(id):
    person = People.query.get_or_404(id)
    db.session.delete(person)
    db.session.commit()
    return jsonify({"message": "Person deleted"})


# GROUP ITEM

@app.route('/group_items', methods=['POST'])
@jwt_required()
def create_group_item():
    data = request.get_json()
    new_group_item = GroupItem(**data)
    db.session.add(new_group_item)
    db.session.commit()
    return jsonify({"message": "Group item created", "group_item": new_group_item.serialize()}), 201

@app.route('/group_items', methods=['GET'])
@jwt_required()
def get_group_items():
    group_items = GroupItem.query.all()
    return jsonify([group_item.serialize() for group_item in group_items])

@app.route('/group_items/<int:id>', methods=['GET'])
@jwt_required()
def get_group_item(id):
    group_item = GroupItem.query.get_or_404(id)
    return jsonify(group_item.serialize())

@app.route('/group_items/<int:id>', methods=['PUT'])
@jwt_required()
def update_group_item(id):
    group_item = GroupItem.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(group_item, key, value)
    db.session.commit()
    return jsonify({"message": "Group item updated", "group_item": group_item.serialize()})

@app.route('/group_items/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_group_item(id):
    group_item = GroupItem.query.get_or_404(id)
    db.session.delete(group_item)
    db.session.commit()
    return jsonify({"message": "Group item deleted"})


# ROLES

@app.route('/roles', methods=['POST'])
@jwt_required()
def create_role():
    data = request.get_json()
    new_role = Role(**data)
    db.session.add(new_role)
    db.session.commit()
    return jsonify({"message": "Role created", "role": new_role.serialize()}), 201

@app.route('/roles', methods=['GET'])
@jwt_required()
def get_roles():
    roles = Role.query.all()
    return jsonify([role.serialize() for role in roles])

@app.route('/roles/<int:id>', methods=['GET'])
@jwt_required()
def get_role(id):
    role = Role.query.get_or_404(id)
    return jsonify(role.serialize())

@app.route('/roles/<int:id>', methods=['PUT'])
@jwt_required()
def update_role(id):
    role = Role.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(role, key, value)
    db.session.commit()
    return jsonify({"message": "Role updated", "role": role.serialize()})

@app.route('/roles/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_role(id):
    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    return jsonify({"message": "Role deleted"})



# LOGIN

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = People.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid email or password"}), 401

    access_token = create_access_token(identity=user.id, additional_claims={"is_admin": user.is_admin})
    
    csrf_token = generate_csrf()  # Generate CSRF token
    
    resp = make_response(jsonify({"message": "Logged in"}))
    resp.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='None')
    resp.set_cookie('csrf_token', csrf_token, httponly=False, secure=True, samesite='None')  # Set CSRF token in cookie
    resp.set_cookie('is_admin', str(user.is_admin), httponly=True, secure=True, samesite='None')

    return resp


# SIGNUP


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    # Check if email already exists in database
    existing_user = People.query.filter_by(email=data['email']).first()
    if existing_user:
        return make_response(jsonify({"message": "Email already exists!"}), 400)

    # Create a new user and set their password
    new_user = People(email=data['email'], person_name=data['name'])  # assuming person_name and other details are in the request
    new_user.set_password(data['password'])  # hashes and sets the password

    # Add other fields if needed from the request data
    # ...

    # Add the user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201


# STATISTICS
@app.route('/statistics', methods=['GET'])
@jwt_required()
def get_statistics():
    total_assets = db.session.query(Asset).count()
    total_users = db.session.query(People).count()
    
    return jsonify({
        "total_assets": total_assets,
        "total_users": total_users
    }), 200


# Check Session

@app.route('/check_session', methods=['GET'])
@jwt_required()
def check_session():
    return jsonify({"authenticated": True}), 200


# Check Admin Status
@app.route('/check_admin_status', methods=['GET'])
@jwt_required()
def check_admin_status():
    current_jwt = get_jwt()
    return jsonify({"is_admin": current_jwt["is_admin"]}), 200



# DEBUGGING

@app.route('/test', methods=['GET'])
def test():
    token = request.cookies.get('access_token')
    try:
        decoded_token = decode_token(token)
        return jsonify({"msg": "Token is valid", "payload": decoded_token})
    except Exception as e:
        return jsonify({"msg": str(e)}), 401
    
@app.route('/test-admin', methods=['GET'])
@jwt_required()
def testAdmin():
    current_jwt = get_jwt()
    
    if not current_jwt["is_admin"]:
        return "Unauthorized", 401
    else :
        return "Authorized", 200



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates the tables in the database
    app.run(debug=True, host='0.0.0.0:$PORT')

