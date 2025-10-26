def test_create_post(client):
    register = client.post("/api/v1/auth/register", json={
        "username": "testuser1",
        "email": "test1@test.com",
        "password": "usertest"
    })
    assert register.status_code == 200
    user_data = register.json()

    login = client.post("/api/v1/auth/login", data={
        "username": "testuser1",
        "password": "usertest"
    })
    assert login.status_code == 200
    token = login.json()["access_token"]

    response = client.post(
        "/api/v1/posts/",
        json={"title": "Test Post", "content": "Post string"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Post"
    assert data["content"] == "Post string"
    assert data["author_id"] == user_data["id"]

def test_get_posts(client):
    register = client.post("/api/v1/auth/register", json={
        "username": "testuser2",
        "email": "test2@test.com",
        "password": "usertest"
    })
    login = client.post("/api/v1/auth/login", data={
        "username": "testuser2",
        "password": "usertest"
    })
    token = login.json()["access_token"]

    client.post(
        "/api/v1/posts/",
        json={"title": "Test Post", "content": "Post string"},
        headers={"Authorization": f"Bearer {token}"}
    )

    response = client.get("/api/v1/posts/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Post"