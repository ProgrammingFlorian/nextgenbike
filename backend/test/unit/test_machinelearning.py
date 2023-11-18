import machinelearning as ml


def test_predict_no_data():
    prediction = ml.predict_on_data("{}")

    assert prediction == []
