# Songwriter Index

## Update: 10/08/18

I've acquired the data necessary to perform a thorough EDA, and, at the very least, determine whether I'll be able to finish this model and subsequent analysis by October 22nd. The biggest issue in potentially preventing me from achieving that goal lies with the songwriter data that I'm able to match to each song I'm working with. I'm still pulling all of the necessary songwriter credits, however, I should be completed with that by this coming Thurs Oct. 11th.

Nonetheless, I'm currently engaging in EDA to determine the viability of this model. I expect to be complete with EDA, and moving onto the modeling stage by this coming Saturday, Oct. 13th.

Outside of whether I'll have enough good songwriter data to complete this project, the biggest obstacles to completing a great project on time rely *on time*. I don't have much time to play around with different models, though I'll try and fit multiple models with my local computer and AWS instance. 

Through the end of the week, I'll be focusing on merging the data I have, conducting additional EDA, and beginning the modeling process. I expect to have a production-ready model by October 15th, and from then on, I'll focus on analysis and interpreting my findings.

Time permitting, I'll begin working on a couple of different stretch goals:
1. Ingesting more song observations, potentially up to 50k songs
2. Developing a website for people to use the tool themselves.

---
## Problem Statement: 
*Develop a model, which given a recording written by a particular songwriter
 or songwriters, can recommend similar sounding recordings written
 by different songwriters, and provide additional background information
 on those other songwriters to interested listeners*

## Background:

While performing artists may enjoy household name recognition, and earnings to
boot, the same cannot be said for the songwriters who pen many of their hit
songs. And, while fame may not be something that a songwriter looks for in their
career, I believe this lack of recognition has also harmed their pocketbook.
Songwriters and music publishers are often the last to negotiate with digital
services to license their music, which leaves the majority of the revenue for
artists and record labels to collect.

I'd like to build a tool which could help fans discover new music, based on
what they're currently listening to. However, instead of putting the artist
front-and-center in the recommendation, I'd like to give fans a glimpse at those
who wrote the hit song.

### Proposed Methods:

In order to create this model, I'll need a dataset comprised of recording 
metadata, with each observation consisting of the following information:

1. Song Title
2. Performing Artist Name(s)
3. Songwriter Credits
4. Audio Features - *from Spotify API*
5. Audio Analysis - *from Spotify API*

I've begun gathering, and will need to gather data from several different
sources, outlined below (access method in parenthesis):

- RIAA (Website): I've scrapped the RIAA Gold and Platinum tables for every artist
who has ever received a US sales award (Gold, Platinum, Diamond, etc). These artists'
songs will make up the sample that I build this recommendation system off of.
- Spotify (API): For recording metadata, including items 1, 2, 4, & 5. Specifically,
I will be using the `Spotipy` wrapper to access this API.
- Genius (API): For songwriter credits. I will be using the `LyricsGenius` wrapper
to access this API. 
  - If the Genius API does not feature enough songwriter credits, I will have
to gather data from a secondary resource. Below are some potential avenues:
    - ISWC-Net (Website)
    - ASCAP (csv)

### Proposed Models:

I will first look to use a recommender system, perhaps implementing a neighborhood
algorithm to recommend new song titles based on the initial song's cosine similarity. I
have not finalized this, however, and may look to use different models based on what
I'm able to see during the EDA process.

### Risks

Given the state of songwriter data, there are a number of risks posed with
embarking on a project like this:
- None of the sources of songwriter data are complete enough to match with
the recording data.
- One or more data sources are far more difficult to clean then realized
previously.
- Matching the recording and songwriter data through programmatic means
results in a fairly large number of erroneous matches, making modeling and
prediction impossible.
