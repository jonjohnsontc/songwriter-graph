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
  - Likely cosine similarity matrix b/w the two (unless i have the math wrong)
- Means of mapping songwriters to one another
  - Likely cosine (or other distance metric)
- Audio analysis for remaining tracks that I don't yet have
- For future: means of scraping additional PRO websites
- Deduplicating songwriters 
  - Likely can do this if I can find publicly available IPI-Base Number database
- Song Lyrics
  - Deciding how to incorporate song lyrics
  - Could decide to only retrieve lyrics for the songs I can actually recommend on?
- Figuring out how tracks should be pulled going forward
- Re-doing functions to make them more efficient (i.e., grabbing means / variances of necessary things)


## 3. Plan
- Complete Preprocessing
- Song to Song Model?
- Complete Songwriter Preprocessing + Modeling Decision
- Complete Songwriter modeling
- Begin Work on New Song Capturing

## 4. Additional Ideas
- Provide each songwriters most frequent collaborators (could be made with jaccard maybe)?


## 5. Modeling Strategies

### 5a. Weighting
- Take each songwriter & divide each of their works by their average work (to make their songs closer in space to one another, and further from frequent collaborators)
- $$ ===

