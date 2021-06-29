# Project Plan - Pulling More Tracks from Spotify

I'd like to start steadily pulling tracks from spotify's api again. I want to build a song dataset that is diverse and reflects how people are listening to music now. 

- I think my approach should be playlist based
  - Pulling songs from hot playlists per country?
  - Pulling associated artist full catalogs?
  - How would I capture older songs? (2019-2020)
    - Pulling associated artist catalog results

- I might be able to use `snapshot_id` to check in the future for changes to playlists

## What do I need per track?

- To match current song dataset
  - tracks
  - audio features
  - audio analysis
- To store all available track data

## Category Based Pulling

- At some cadence (weekly?)
- Pull all categories in all markets
  - Pull associated playlists for each category
    - I get track data from that
    - Pull associated audio features for each track
    - Pull associated audio analysis for each track (LATER)
      - Should I leave this for later? Since it's so data intensive? Like, only pull if we match to a songwriter record?

### Category Based Pulling - Updates

 