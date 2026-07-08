# Plan: Weighted content-based scoring + ranking rule for the recommender

## Context

`src/recommender.py` has two parallel, unimplemented surfaces that both need the
same underlying math:

- **OOP surface** (tested by `tests/test_recommender.py`): `Song` / `UserProfile`
  dataclasses, `Recommender.recommend()` and `Recommender.explain_recommendation()`.
- **Functional surface** (used by `src/main.py`): `load_songs()`, `score_song()`,
  `recommend_songs()`, driven by plain dicts (`user_prefs = {"genre", "mood",
  "energy"}`, optionally `"acousticness"`/`"likes_acoustic"`).

Right now both just return placeholders/slices with no real scoring. The goal of
this plan is to define **one shared mathematical scoring rule** — with explicit
per-feature weights reflecting how strong a signal each feature is — and a
**ranking rule**, then implement both against it so the two surfaces produce
consistent, explainable results and the existing tests pass.

Data available per song (`data/songs.csv`): `genre`, `mood` (categorical),
`energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness` (continuous,
mostly 0–1 except `tempo_bpm`). User preferences only ever specify
`genre`, `mood`, `energy`, and acoustic preference — so the formula is built on
those four; `tempo_bpm`/`valence`/`danceability` are not used since no user-facing
preference exists for them today (documented as a future extension, not built).

## Scoring rule

For a song `s` and user preference `u`, compute a weighted sum of four
sub-scores, each normalized to `[0, 1]`:

| Component | Sub-score formula | Weight | Rationale |
|---|---|---|---|
| Genre match | `1.0 if s.genre.lower() == u.genre.lower() else 0.0` | **0.35** | Strongest, most explicit preference signal — categorical and binary. |
| Mood match | `1.0 if s.mood.lower() == u.mood.lower() else 0.0` | **0.25** | Second strongest explicit signal, also categorical. |
| Energy closeness | `1.0 - abs(s.energy - u.target_energy)` | **0.25** | Continuous; rewards proximity rather than exact match since energy is a dial, not a category. |
| Acoustic match | `1.0 if (s.acousticness >= 0.5) == u.likes_acoustic else 0.0` | **0.15** | Weakest signal — binary preference derived by thresholding a continuous attribute at 0.5. |

`score = 0.35*genre + 0.25*mood + 0.25*energy + 0.15*acoustic` → always in `[0, 1]`,
weights sum to 1.0.

**Missing preference handling (functional/dict surface only):** `user_prefs` may
omit `acousticness`/`likes_acoustic` (as in `src/main.py`'s example). When a key
is absent, drop that term and **renormalize the remaining weights** to sum to 1
(e.g., without the acoustic term: `genre/0.85, mood/0.85, energy/0.85` scaled
weights) rather than silently scoring it as 0 — an absent preference should be
neutral, not a penalty.

**Explanation reasons:** each component that meets its match condition (or, for
energy, is within a small tolerance e.g. `<=0.15` diff) contributes a short
human-readable reason string, e.g. `"matches favorite genre (pop)"`,
`"close to target energy (0.8 vs 0.82)"`. `score_song` returns `(score, reasons)`;
`explain_recommendation` joins reasons into one sentence (or returns a fallback
sentence like `"generally aligned with your taste"` if no component matched, so
the string is never empty).

## Ranking rule

1. Score every song against the user preference using the rule above.
2. Sort descending by score.
3. **Tie-break** deterministically on a secondary key — recommend `s.valence`
   descending (favor the more universally-appealing track), falling back to
   `s.id` ascending for full determinism.
4. Return the top `k`.

This applies identically to `Recommender.recommend()` (returns `List[Song]`) and
`recommend_songs()` (returns `List[Tuple[dict, float, str]]`).

## Files to change

- `src/recommender.py`:
  - `score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]`: implement
    the weighted formula above over dicts, with the missing-key renormalization.
  - `recommend_songs(...)`: call `score_song` for every song, sort per the ranking
    rule, build explanation strings, return top `k` tuples.
  - `load_songs(csv_path)`: parse the CSV (`csv.DictReader`) into `List[Dict]`,
    casting numeric fields (`energy`, `tempo_bpm`, `valence`, `danceability`,
    `acousticness`) to `float`.
  - `Recommender.recommend()`: reuse the same math against `Song`/`UserProfile`
    dataclass fields (`favorite_genre`, `favorite_mood`, `target_energy`,
    `likes_acoustic` — always present on the dataclass, so no renormalization
    branch needed here).
  - `Recommender.explain_recommendation()`: reuse the same reason-string logic.

No new files or dependencies needed — everything reuses the existing dataclasses
and stub signatures already required by `tests/test_recommender.py` and
`src/main.py`.

## Verification

- `pytest tests/test_recommender.py -v` — confirms `recommend()` ranks the
  pop/happy song first and `explain_recommendation()` returns a non-empty string.
- `python -m src.main` (from repo root) — with the starter profile
  `{"genre": "pop", "mood": "happy", "energy": 0.8}` against `data/songs.csv`,
  confirms "Sunrise City" (pop, happy, energy 0.82) and "Gym Hero" (pop, intense,
  energy 0.93) rank at the top, and that printed scores are in `[0, 1]` with
  sensible "Because: ..." explanations.
