# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: Sensation Recommendation 

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 
This recommendation tool is used for avid music listeners who have access to a collection of songs and their content-based attributes. Users would input their preferences across multiple aspects of music, and from their dataset a ranking system would be made to recommend them k number of songs to try out.

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  
Genre and mood are the 2 largest indicators of preference according to my Model. Both are also boolean values, contributing a score of 0 or 1, which is weighted highly (about 0.7 of total score). Lower weights include an energy and acousticness score, which is entered as a float and weighted at a lower value than the first 2 (about 0.3 of total score).

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  
The dataset features 20 songs (I added 10) from various genres, moods, and artists. It came in the form of csv (easy to use in Python), and each song has many content-based features such as genre, mood, energy, tempo, etc.

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  
My system performs especially well after checking edge cases, including unique user preferences and unexpected inputs. It also scores strongly on recommendations that match the user's genre of choice.

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 
The model really only considers the 4 main features mentioned above, and it's limitations include a lack of language consideration, small training set, and knowledge of only mainstream genres. It would be very harsh on more niche music, which could prevent the user from expanding their taste as their known songs base increases. One more thing is that it doesn't consider explicit music ratings, which could be harmful especiailly if young people are using the tool.

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 
I created a few user profiles of my own, and then asked Claude Code for unexpected user behavior and edge case inputs that could either break the program or silently pass a test incorrectly (false positive)
What surprised me most was that a couple of "shouldn't happen" inputs (huge energy numbers, stray spaces like " pop") didn't crash the program, but instead silently produced a worse or invalid recommendation (including scores that could go negative). Those are the worst bugs, since nothing looks broken until you compare outputs side by side. Fixed it by capping the energy score at zero and trimming whitespace before comparing genre/mood text.

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  
I would significantly expand the dataset in terms of songs to choose from, and features to consider. Then I would include these features in my score calculation, which should create a more diverse recommendation set for the user. I would also run an error metric to compare a real user's enjoyed songs from their recommendation, to analyze the model's precision and recall, and see which they would rather get (FP or TN)

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

These systems require lots of pieces of data, and plenty of data about that data. The more information a model has the better, as it can make more accurate predictions based off its knowledge base. This is also a much more harmless example of the precision vs recall tradeoff, because whether a user misses out on a good recommendation or finds that they don't like a recommendation, no one is really hurt in the end. However, I'm now curious about how some of the software, like for a generated playlist for you, chooses whether to recommend songs you've played or new songs. I wonder this because I feel like Spotify recommends me the same songs some times.