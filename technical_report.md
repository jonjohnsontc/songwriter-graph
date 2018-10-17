
# SongIndex

SongIndex is the first step in a process to connect listeners to songwriters through machine learning. The first step, which is designed to address the following problem:

> Can we build a recommender system to connnect listeners, given them providing a song title (and without prior listenership data), with new music which sounds very similar to the title provided?

I believe the model constructed here addresses this problem. 

You're welcome to read the `Methodology` section below, which outlines all of the steps taken in the process to build this recommender, or dive directly into the `notebooks` folder, which runs through each step thoroughly with code and plots to help illustrate.

## Methodology

Using cosine similarity, I analyzed roughly 22000 song titles utilizing their corresponding Audio Features and Audio Analysis, as well as genre information tied to the songs performing artist, all obtained through the Spotify API, utilizing a Python wrapper aptly named Spotipy.

Every song was ~rated~ on its similarity with the other recordings through the features contained in the aforementioned documents, along with some features that had been engineered through a combination of other features, which resulted in a total list of 74 song attributes, a complete listing of  which can be found in the TK notebook and data dictionary file. You'll find a summary of each meta-feature section (meta-feature relating to the original area of the Spotify API where the feature was found) below.

### Audio Features 


### Audio Analysis

### Artist Genres

### Why Cosine Similarity?

Cosine Similarity is the normalized dot product ..., and can be written as such:

$$cos(\theta) = \frac{A * B}{A

The short of this is: Because it provided results that sounded the most similar to songs provided in testing.

I think intuitively, that Euclidean distance makes more sense when trying to measure the similarity of songs using the feature sets that are incorporated here, wherein the most of the features are measurements centered around zero. However, in aggregate, the test results using Cosine similarity sounded closer to the original titles provided than the results utilizing euclidean distance. The songs recommended through cosine similarity were also more diverse, in terms of the performing artist. Wherein, usine euclidean distance, there was a higher frequency of the same artist who 

Cosine similarity is also 

### Results

## Updates to Come

In the near future, I plan on adding a number of additions, including 

- Web interface to query API for recommendations
- Incorporate songwriter credits into the model
- Add additional titles, starting with new releases through Spotify's web API

Eventually, I plan on revamping the recommender entirely, into the aforementioned tool to connect listeners with songwriters. The idea of the model being two-fold (and therefore made up of two different models):

- Given a song, recommend songwriters whom write similarly to how the song in question was written
- Recommend the songwriter's works which sound most like the original song submitted



