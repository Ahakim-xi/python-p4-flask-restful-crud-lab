import pytest
from server.app import app, db, Plant

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
        db.session.remove()
        db.drop_all()

def test_get_plants_empty(client):
    response = client.get('/plants')
    assert response.status_code == 200
    assert response.get_json() == []

def test_post_plant(client):
    data = {
        'name': 'Monstera',
        'image': 'monstera.jpg',
        'price': 25.0,
        'is_in_stock': True
    }
    response = client.post('/plants', json=data)
    assert response.status_code == 201
    plant = response.get_json()
    assert plant['name'] == 'Monstera'
    assert plant['image'] == 'monstera.jpg'
    assert plant['price'] == 25.0
    assert plant['is_in_stock'] is True

def test_get_plant_by_id(client):
    plant = Plant(name='Jade', image='jade.jpg', price=15.0, is_in_stock=True)
    db.session.add(plant)
    db.session.commit()
    response = client.get(f'/plants/{plant.id}')
    assert response.status_code == 200
    result = response.get_json()
    assert result['name'] == 'Jade'

def test_patch_plant(client):
    plant = Plant(name='Pothos', image='pothos.jpg', price=10.0, is_in_stock=True)
    db.session.add(plant)
    db.session.commit()
    response = client.patch(f'/plants/{plant.id}', json={'price': 12.0, 'is_in_stock': False})
    assert response.status_code == 200
    updated = response.get_json()
    assert updated['price'] == 12.0
    assert updated['is_in_stock'] is False

def test_delete_plant(client):
    plant = Plant(name='ZZ Plant', image='zz-plant.jpg', price=20.0, is_in_stock=True)
    db.session.add(plant)
    db.session.commit()
    response = client.delete(f'/plants/{plant.id}')
    assert response.status_code == 204
    assert db.session.get(Plant, plant.id) is None
