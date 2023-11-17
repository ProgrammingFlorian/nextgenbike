from test.unit.app import client


def test_landing_page(client):
    landing_page = client.get("/")
    html = landing_page.data.decode()

    assert landing_page.status_code == 200
    assert "Welcome to the Next-Gen Bike backend!" in html
