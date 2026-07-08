import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

NUMERIC_FIELDS = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")

GENRE_WEIGHT = 0.35
MOOD_WEIGHT = 0.25
ENERGY_WEIGHT = 0.25
ACOUSTIC_WEIGHT = 0.15
ENERGY_CLOSE_TOLERANCE = 0.15
ACOUSTIC_CLOSE_TOLERANCE = 0.15

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: float

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Store the candidate songs to recommend from."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs for a user, ranked by score."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable reason a song was recommended to a user."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dicts with numeric fields cast to float."""
    songs = []
    with open(csv_path, newline="") as csv_file:
        for row in csv.DictReader(csv_file):
            row["id"] = int(row["id"])
            for field in NUMERIC_FIELDS:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences via weighted genre/mood/energy/acoustic components."""
    components = []

    pref_genre = user_prefs.get("genre")
    if pref_genre is not None:
        match = str(song["genre"]).lower() == str(pref_genre).lower()
        reason = f"matches favorite genre ({song['genre']})" if match else None
        components.append((GENRE_WEIGHT, 1.0 if match else 0.0, reason))

    pref_mood = user_prefs.get("mood")
    if pref_mood is not None:
        match = str(song["mood"]).lower() == str(pref_mood).lower()
        reason = f"matches favorite mood ({song['mood']})" if match else None
        components.append((MOOD_WEIGHT, 1.0 if match else 0.0, reason))

    pref_energy = user_prefs.get("energy")
    if pref_energy is not None:
        diff = abs(float(song["energy"]) - float(pref_energy))
        reason = (
            f"close to target energy ({pref_energy} vs {song['energy']})"
            if diff <= ENERGY_CLOSE_TOLERANCE
            else None
        )
        components.append((ENERGY_WEIGHT, 1.0 - diff, reason))

    pref_acoustic = user_prefs.get("acousticness", user_prefs.get("likes_acoustic"))
    if pref_acoustic is not None:
        diff = abs(float(song["acousticness"]) - float(pref_acoustic))
        reason = (
            f"acousticness matches your preference ({song['acousticness']})"
            if diff <= ACOUSTIC_CLOSE_TOLERANCE
            else None
        )
        components.append((ACOUSTIC_WEIGHT, 1.0 - diff, reason))

    if not components:
        return 0.0, []

    total_weight = sum(weight for weight, _, _ in components)
    score = sum(weight * subscore for weight, subscore, _ in components) / total_weight
    reasons = [reason for _, _, reason in components if reason]
    return score, reasons

FALLBACK_EXPLANATION = "generally aligned with your taste"

def _format_explanation(reasons: List[str]) -> str:
    """Join reason strings into one sentence, or a fallback if there are none."""
    return "; ".join(reasons) if reasons else FALLBACK_EXPLANATION

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song against user preferences and return the top k, ranked descending."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    ranked = sorted(
        scored,
        key=lambda entry: (-entry[1], -entry[0]["valence"], entry[0]["id"]),
    )
    return [(song, score, _format_explanation(reasons)) for song, score, reasons in ranked[:k]]
