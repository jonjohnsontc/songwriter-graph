# SongWriter Index - Remaining Project Plan

Date: 2/16/19

Steps outlined will be numbered from days after the date above.

## Table of Contents
1. Current Resources
2. Additional Resources Needed
3. Step-by-Step Plan

## 1. Current Resources
- > 450k Song Registrations from ASCAP
- ~650k track details from Spotify API
- Framework for matching tracks to compositions
  - Enough for ~150k potential songs to match on
  - Enough for ~10k potential songwriters to match on
- Cosine similarity matrix for 24k tracks

## 2. Additional Resources Needed
- Means of recommending songwriters given a song
  - Could you perform LDA on EVERYTHING?
    - Then, for every song, a given author would have a collection of "topics" that would relate to them
  - PCA on each song?
- Means of recommending songs from given songwriters
- Audio analysis for remaining tracks that I don't yet have
- For future: means of scraping additional PRO websites
- Deduplicating songwriters 
  - Likely can do this if I can find publicly available IPI-Base Number database
- Song Lyrics
  - Deciding how to incorporate song lyrics
  - Could decide to only retrieve lyrics for the songs I can actually recommend on?

## 3. Plan
2/16 - Continue Pulling Audio Analysis & Start Ideating on Modeling Strats
2/17 - Continue Pulling Audio Analysis 
2/18 - Continue Pulling Audio Analysis
2/19 - Finish Pulling Audio Analysis
2/20 - Migrate Files from EC2 unto external drive
5. Begin modeling search
a. reach out to people on Automation COP
6. Synthesize new dataset
7. Construct small modeling tests

