def test_register_user(client):
    response = client.post("/api/v1/auth/register", json={
        "username": "testuser3",
        "email": "test3@test.com",
        "password": "usertest"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser3"
    assert data["email"] == "test3@test.com"
    assert "id" in data

def test_login_user(client):
    client.post("/api/v1/auth/register", json={
        "username": "testuser4",
        "email": "test4@test.com",
        "password": "usertest"
    })
    
    response = client.post("/api/v1/auth/login", data={
        "username": "testuser4",
        "password": "usertest"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
