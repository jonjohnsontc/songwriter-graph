# Revised Capstone - SongIndex

Given that the integrity of the songwriter data that I've extracted isn't great, I cannot be confident in the ability of a recommender making songwriter based predictions. However, I can still make recommendations on similar songs based on the structure of their compositions. I call this recommender, and the underlying data that powers it *SongIndex*.

## Revised Problem Statement


## Methodology
The data I'm using in this model comes from Spotify's API, and consists of *Audio Features* and *Audio Analysis* for approximately 20,000 tracks. These tracks represent the top 10 most popular recordings (as of 10/2/2018) of every artist that has earned at least one RIAA sales award (as of 9/22/2018).

The key in making these predictions will be focusing on the elements of the song's underlying composition, as opposed to elements of an entire recording. Therefore, it's important to distinguish out of the features that I have, which of those correspond to the song itself, and which are more related to the elements of the recording.

### Elements of a Composition
There is not a 

### Elements of a Recording

### Song Features Involved in Model

- Capture when either Key Change occurs, or the total number of keys utilized over the course of the work