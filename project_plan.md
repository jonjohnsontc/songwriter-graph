# SongWriter Index - Remaining Project Plan

Original Date: 2/16/19  

Last Updated: 5/30/19

Steps outlined will be numbered from days after the date above.

## Table of Contents
1. Current Resources
2. Additional Resources Needed
3. Step-by-Step Plan

## 1. Current Resources
- > 450k Song Registrations from ASCAP
- ~650k track details from Spotify API
- 2 nearest neighbor models, each recommending roughly 10k songwriters
  1. Based on Manhattan Distance
  2. Based on Euclidean Distance
- Cosine similarity matrix for 24k tracks

## 2. Additional Resources Needed
- Continuously ingesting new songs
- Means of describing how a songwriter writes
  - 40 person panel OR
  - perhaps just interviewing a few experts and heavy+light fans (10)
- Means of recommending songwriters given a song
  - Could you perform LDA on EVERYTHING?
    - Then, for every song, a given author would have a collection of "topics" that would relate to them
  - PCA on each song?
- Means of recommending songs from given songwriters
  - Likely cosine similarity matrix b/w the two (unless i have the math wrong)
- Means of scraping additional PRO websites
- Deduplicating songwriters 
  - Likely can do this if I can find publicly available IPI-Base Number database
  - Should also focus on cleaning them myself if I can't work with JAAK
- Song Lyrics
  - Deciding how to incorporate song lyrics
  - Could decide to only retrieve lyrics for the songs I can actually recommend on?
- Figuring out how tracks should be pulled going forward
- Re-doing functions to make them more efficient (i.e., grabbing means / variances of necessary things)

## 3. Plan
- Calculate Jaccard Similarity for Current Model
-  

## 4. Additional Ideas
- Provide each songwriters most frequent collaborators (could be made with jaccard maybe)?


