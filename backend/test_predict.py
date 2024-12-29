from ml.predict import predict_song_removal

def test_keep_prediction():
    """
    Test a case where the model should predict 'Keep'.
    """
    # Example input: high popularity, low age, good genre alignment
    features = [80, 2, 60, 20, 0.8]  # [popularity, age, avg_playlist_popularity, relative_popularity, genre_alignment_score]
    genre = "pop"
    prediction = predict_song_removal(features, genre)
    assert prediction == 0, "Expected 'Keep' (0), but got 'Remove' (1)"
    print("Test Passed: Keep Prediction")


def test_remove_prediction():
    """
    Test a case where the model should predict 'Remove'.
    """
    # Example input: low popularity, high age, poor genre alignment
    features = [30, 10, 60, -30, 0.2]  # [popularity, age, avg_playlist_popularity, relative_popularity, genre_alignment_score]
    genre = "rock"
    prediction = predict_song_removal(features, genre)
    assert prediction == 1, "Expected 'Remove' (1), but got 'Keep' (0)"
    print("Test Passed: Remove Prediction")


def test_unknown_genre():
    """
    Test a case where the genre is unknown to the encoder.
    """
    # Example input: medium popularity, average age, unknown genre
    features = [50, 5, 60, -10, 0.5]  # [popularity, age, avg_playlist_popularity, relative_popularity, genre_alignment_score]
    genre = "unknown_genre"
    prediction = predict_song_removal(features, genre)
    assert prediction in [0, 1], "Prediction must be either 'Keep' (0) or 'Remove' (1)"
    print(f"Test Passed: Unknown Genre Prediction ({'Remove' if prediction == 1 else 'Keep'})")


def test_edge_case_low_popularity_high_alignment():
    """
    Test a case where popularity is low but genre alignment is high.
    """
    features = [20, 8, 60, -40, 1.0]  # Low popularity but perfect genre alignment
    genre = "pop"
    prediction = predict_song_removal(features, genre)
    assert prediction in [0, 1], "Prediction must be either 'Keep' (0) or 'Remove' (1)"
    print(f"Test Passed: Low Popularity, High Alignment Prediction ({'Remove' if prediction == 1 else 'Keep'})")


def run_tests():
    """
    Run all test cases.
    """
    print("Running Tests...")
    test_keep_prediction()
    test_remove_prediction()
    test_unknown_genre()
    test_edge_case_low_popularity_high_alignment()
    print("All Tests Passed!")


if __name__ == "__main__":
    run_tests()
