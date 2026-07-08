"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def print_recommendations(label: str, songs, user_prefs: dict, k: int = 5) -> None:
    print(f"\n{'=' * 70}")
    print(f"{label}")
    print(f"prefs={user_prefs} k={k}")
    print("-" * 70)
    recommendations = recommend_songs(user_prefs, songs, k=k)
    if not recommendations:
        print("  (no recommendations)")
        return
    for song, score, explanation in recommendations:
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Starter example profiles
    profiles = [
        ("Pop / happy / energetic", {"genre": "pop", "mood": "happy", "energy": 0.8}),
        ("Rock / sad / mid-energy", {"genre": "rock", "mood": "sad", "energy": 0.5}),
        ("Jazz / relaxed / chill", {"genre": "jazz", "mood": "relaxed", "energy": 0.3}),
    ]
    for label, prefs in profiles:
        print_recommendations(label, songs, prefs)

    # Edge case profiles: designed to probe whether the scoring/ranking
    # logic can be tricked or produce unexpected results.
    edge_cases = [
        ("Edge case: empty preferences", {}, 5),
        (
            "Edge case: nothing in the dataset matches genre/mood",
            {"genre": "polka", "mood": "furious", "energy": 0.5},
            5,
        ),
        (
            "Edge case: energy preference out of [0, 1] range (high)",
            {"genre": "pop", "mood": "happy", "energy": 2.0},
            5,
        ),
        (
            "Edge case: energy preference out of [0, 1] range (negative)",
            {"genre": "pop", "mood": "happy", "energy": -1.0},
            5,
        ),
        (
            "Edge case: uppercase genre/mood (case sensitivity check)",
            {"genre": "POP", "mood": "HAPPY", "energy": 0.8},
            5,
        ),
        (
            "Edge case: whitespace-padded genre/mood",
            {"genre": " pop", "mood": "happy ", "energy": 0.8},
            5,
        ),
        ("Edge case: only likes_acoustic=True given", {"likes_acoustic": True}, 5),
        ("Edge case: only likes_acoustic=False given", {"likes_acoustic": False}, 5),
        (
            "Edge case: likes_acoustic=0 (falsy int, must not be treated as absent)",
            {"likes_acoustic": 0},
            5,
        ),
        (
            "Edge case: both acousticness and likes_acoustic given (acousticness should win)",
            {"genre": "pop", "acousticness": 0.9, "likes_acoustic": False},
            5,
        ),
        ("Edge case: k=0", {"genre": "pop", "mood": "happy", "energy": 0.8}, 0),
        ("Edge case: negative k", {"genre": "pop", "mood": "happy", "energy": 0.8}, -1),
        (
            "Edge case: k larger than the number of songs available",
            {"genre": "pop", "mood": "happy", "energy": 0.8},
            100,
        ),
        (
            "Edge case: explicit None values instead of absent keys",
            {"genre": None, "mood": None, "energy": None},
            5,
        ),
        (
            "Edge case: energy passed as a numeric string",
            {"genre": "pop", "mood": "happy", "energy": "0.8"},
            5,
        ),
        (
            "Edge case: unrelated extra keys should be ignored",
            {"genre": "pop", "favorite_color": "blue", "energy": 0.8},
            5,
        ),
    ]
    for label, prefs, k in edge_cases:
        print_recommendations(label, songs, prefs, k=k)


if __name__ == "__main__":
    main()
