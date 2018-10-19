
# SongIndex

SongIndex is the first step in a process to connect listeners to songwriters through machine learning. The first step, which is designed to address the following problem:

## Problem Statement:

> Can we build a recommender system to connnect listeners, given them providing a song title (and without prior listenership data), with different music which sounds very similar to the title provided?

I believe the model constructed here addresses this problem, though I do believe it can improve significantly with the inclusion of a larger dataset (more songs), along with additional features, like song lyrics. 

You're welcome to read the `Executive Summary` section below, which outlines the steps taken in the process to build this recommender, or dive directly into the `technical_report_nbs` folder, which runs through each step thoroughly with code and plots to help illustrate.

## Executive Summary 

Using cosine similarity, I analyzed roughly 22000 song titles utilizing their corresponding Audio Features and Audio Analysis, as well as genre information tied to the songs performing artist, all obtained through the Spotify API, utilizing a Python wrapper aptly named Spotipy.

Every song was measured on its similarity with the other recordings through the features contained in the aforementioned documents, along with some features that had been engineered through a combination of other features, which resulted in a total list of 74 song attributes, a complete listing of which can be found in the `03_preprocessing` notebook and `data_dictionary.txt` file. 

### Results

Here are a few example results to help illustrate the efficacy of this recommender:

#### "Clique" by Kanye West

|Song Name|Artist|Similarity|
|---|---|---|
|Willy Wonka (feat. Offset)|Macklemore|0.776872|
|3005|Childish Gambino|0.689925
|Ladders|Mac Miller|0.660775|
|Ghost Town|Kanye West|0.641954|
|Thrift Shop (feat. Wanz)|Macklemore & Ryan Lewis|0.640089|
|No Role Modelz|J. Cole|0.636222|
|Don't Like.1|Kanye West|0.634637|
|Freaks And Geeks|Childish Gambino|0.62986|
|By Design|Kid Cudi|0.628633|
|Renegade|JAY Z|0.61611|

#### "With Arms Wide Open" by Creed

|Song Name|Artist |Similarity|
|---|---|---|
|Anthem for the Year 2000|Silverchair|0.688038|
|Bittersweet|Fuel|0.684205|
|I Can Still Feel You (feat. Thompson Square)|Blues Traveler|0.664157|
|Spotlights|Candlebox|0.613167|
|Sunburn|Fuel|0.611922|
|Swallowed|Bush|0.605053|
|The Mountains Win Again|Blues Traveler|0.604242|
|Cover Me|Candlebox|0.603657|
|Lost In You|Bush|0.594501|

## Updates to Come

In the near future, I plan on adding a number of additions, including:

- Additional titles, starting with the full catalog of each featured artist 
- A web interface to query the recommender
- Adding song lyrics as an additional set of features
- Incorporating songwriter credits into the model

Eventually, I plan on revamping the recommender entirely, into the aforementioned tool to connect listeners with songwriters. The idea of the model being two-fold (and therefore made up of two different models):

- Given a song, recommend songwriters whom write similarly to how the song in question was written
- Recommend the songwriter's works which sound most like the original song submitted

## Layout 

You'll find this project currently spread over 3 different folders, though this is subject to change with the inclusion of additional content.

- [data](./data) - Where all of the datasets generated are stored
- [pickle](./pickle) - Where all of the pickled variables are stored
- [notebooks](./notebooks) - The notebooks which comprise the technical report (please note that the notebooks prepended with i's are anciallary and are still works in progress, the numbered files which comprise the technical report are finished, however)
- [`data_dictionary.md`](data_dictionary.md) - Where you can find definitions of all the features used in the recommender
- [`requirements.txt`](requirements.txt) - All of the libraries necessary to run through each notebook
- More Requirements.
