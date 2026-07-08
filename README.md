  # 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.
The recommandation machine is content-based, so user's will get recommended songs based on how close the features of a new song line up with their existing preferences. Stronger features (mood, genre) will have more weight in scoring similarity to user preference, while less significant features (acoustic preference) zwill have less of an impact on whether a song should be recommended or not.

Some prompts to answer:

- What features does each `Song` use in your system
  - Primarily genre, mood and energy
- What information does your `UserProfile` store
These 3 plus acoustic preference
- How does your `Recommender` compute a score for each song
It assigns a value to the features used, and applies a scalar weight to compute a composite recommendation score
- How do you choose which songs to recommend
The algorithm will sort the songs by scores in descending order, and return recommendations to the top x songs

You can include a simple diagram or bullet list if helpful.
See file which-features....

Note that this algorithm prioritizes songs that match the user's choice of mood and genre precisely. A song that exactly matches their acoustic preference or energy levels may not be high enough in the rankings even with an exact match.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

Top recommendations:

Sunrise City - Score: 0.99
Because: matches favorite genre (pop); matches favorite mood (happy); close to target energy (0.8 vs 0.82)

Gym Hero - Score: 0.67
Because: matches favorite genre (pop); close to target energy (0.8 vs 0.93)

Rooftop Lights - Score: 0.58
Because: matches favorite mood (happy); close to target energy (0.8 vs 0.76)

Circuit Breaker - Score: 0.29
Because: close to target energy (0.8 vs 0.81)

Night Drive Loop - Score: 0.28
Because: close to target energy (0.8 vs 0.75)


Edge case: explicit None values instead of absent keys
prefs={'genre': None, 'mood': None, 'energy': None} k=5
----------------------------------------------------------------------
Sunrise City - Score: 0.00
Because: generally aligned with your taste

Rooftop Lights - Score: 0.00
Because: generally aligned with your taste

Carnival Static - Score: 0.00
Because: generally aligned with your taste

Gym Hero - Score: 0.00
Because: generally aligned with your taste

Neon Static - Score: 0.00
Because: generally aligned with your taste


======================================================================
Edge case: energy passed as a numeric string
prefs={'genre': 'pop', 'mood': 'happy', 'energy': '0.8'} k=5
----------------------------------------------------------------------
Sunrise City - Score: 0.99
Because: matches favorite genre (pop); matches favorite mood (happy); close to target energy (0.8 vs 0.82)

Gym Hero - Score: 0.67
Because: matches favorite genre (pop); close to target energy (0.8 vs 0.93)

Rooftop Lights - Score: 0.58
Because: matches favorite mood (happy); close to target energy (0.8 vs 0.76)

Circuit Breaker - Score: 0.29
Because: close to target energy (0.8 vs 0.81)

Night Drive Loop - Score: 0.28
Because: close to target energy (0.8 vs 0.75)


======================================================================
Edge case: unrelated extra keys should be ignored
prefs={'genre': 'pop', 'favorite_color': 'blue', 'energy': 0.8} k=5
----------------------------------------------------------------------
Sunrise City - Score: 0.99
Because: matches favorite genre (pop); close to target energy (0.8 vs 0.82)

Gym Hero - Score: 0.95
Because: matches favorite genre (pop); close to target energy (0.8 vs 0.93)

Circuit Breaker - Score: 0.41
Because: close to target energy (0.8 vs 0.81)

Rooftop Lights - Score: 0.40
Because: close to target energy (0.8 vs 0.76)

Night Drive Loop - Score: 0.40
Because: close to target energy (0.8 vs 0.75)

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

Preferences outside of the standardized 0-1 range were resulting in negative scores, which could be useful for the user to specify they would not like to see songs like that
Setting k < 0 was silently working instead of erroring due to pythonic indexing
I ended up switching acousticness from a binary (< or > 0.5) to a float because that attribute isn't really a yes/no question

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

Miniscule dataset, likely will overfit and struggle as niche preferences are addede
Has no regard for language
Attempts to compute subjective values (danceability), risk of bias
Explicit content is never marked/filtered- could be an issue if kids use this tool

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

See model card

