import pytest
import pandas as pd
import os

# Set testing environment variable
os.environ["TESTING"] = "true"

from evaluation.online_evaluation import calculate_precision_at_k, get_user_relevant_movies

@pytest.fixture
def sample_data():
    """Fixture for sample data as DataFrame."""
    data = {
        'user_time': ['2024-10-11T15:07:38', '2024-10-11T15:07:39', '2024-10-11T15:07:40', '2024-10-11T15:07:41'],
        'user_id': [1, 1, 2, 2],
        'movie_id': ['movie1', 'movie2', 'movie1', 'movie3'],
        'movie_title': ['Movie One', 'Movie Two', 'Movie One', 'Movie Three'],
        'year': [2000, 2001, 2000, 2002],
        'rating': [5, 4, 3, 5]
    }
    return pd.DataFrame(data)

def test_get_user_relevant_movies(sample_data):
    """Test the get_user_relevant_movies function."""
    expected_output = {1: {'movie1', 'movie2'}, 2: {'movie3'}}
    relevant_movies = get_user_relevant_movies(sample_data, rating_threshold=4)
    assert relevant_movies == expected_output

def test_calculate_precision_at_k():
    """Test the calculate_precision_at_k function with sample recommendation data."""
    # Sample data for user recommendations and relevant movies
    user_recommendations = {1: ['movie1', 'movie2', 'movie4'], 2: ['movie3', 'movie5', 'movie6']}
    user_relevant_movies = {1: {'movie1', 'movie2'}, 2: {'movie3'}}
    
    # Calculate precision
    precision = calculate_precision_at_k(user_recommendations, user_relevant_movies, k=10)
    
    # Expected precision: (2/10 + 1/10) / 2 = 0.15
    assert precision == pytest.approx(0.15, rel=1e-2)
