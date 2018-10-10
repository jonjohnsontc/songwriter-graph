(taken from https://www.youtube.com/watch?v=goUzHd7cTuA&feature=youtu.be)

# Audio Analysis with the Spotify Web API

Talk given by Mark Koh

## Audio Analysis for the Spotify API could be broken down into two segments:
   - Audio Features (high-level)
   - Audio Analysis (low-level)

## Audio Features:
- Acousticness, Instrumentalness, & Speechiness are attempted binary classifiers for whether a song is acoustic, instrumental, or contains speech.
  - If the speechiness is a 1, I should probably drop it from my analysis
- Valence is how happy or sad a track is -- very subjective
- Liveness: probability distribution on whether a track is performed live
  - Should DEFINITELY be dropped  

## Audio Analysis:
- NOTE: All of these measurements are estimates, so `confidence` should play a role in the modeling process. 
- Tatum: The smallest pulse that a human can perceive (usually around half of a beat)
  - Can be helpful in determining how "swung" a song is. (From Wikipedia) Swing has two main uses in music:
    - Describes the sense of propulsive rhythmic "feel" or "groove".
    - The term is also used more specifically, to refer to a technique that involves alternately lengthening and shortening the pulse-divisions in a rhythm.
- Bars, Beats & Tatums:
  - Each one of these elements comes with:
    - `start` time of the chunk
    - `duration` of the chunk
    - `confidence` of the chunk
- Beat: Basic time unit of a piece of music (e.g., each tick of a metronome)
- Bar: A segment of time defined as a given number of beats. Bar offsets also indicate downbeats, the first beat of the measure.

### Sections:
- Defined by large variations in rhtym or timbre (e.g., chorus, verse, bridge, guitar solo, etc.)
- Each section contains its own descriptions of tempo, key, mode, time_signature, and loudness
- Mark Koh believes they're "not great" (i.e., not super accurate).
  - May work really well for some songs and not others

### Segments:
- A set of sound entities (typically under a second), each relatively uniform in timbre and harmony.
  - i.e., A chunk of time that has generally the same sound throughout.
- Characterized by their perceptual onsets and duration in seconds, loudness, pitch and timbral content.
- Example: If you had a piano song (the only instrument/voice), each note would get it's own segment.
  - In this example, it would be really easy to see how many times the c chord was played on a song.
- Pitch:
  - Given in a 'chroma vector' (length 12)
  - Corresponding to the 12 pitch classes, with values from 0 to 1 that describe the relative dominance of every pitch in the chromatic scale.
    - A c major chord would likely be represented by largevalues of C, E, & G (i.e., classes 0, 4, & 7)
  - Vectors are normalized to 1 by their strongest dimension. 
    - noisy sounds are likely represented by values that are all close to one (this seems really important in differntiating types of music)
    - pure tones are described by one value at 1 (the pitch) and others near 0
- Timbre: How sound works
  - The quality of a musical note or sound that distinguishes different types of musical instruments or voices.
  - Represented as a vectore that includes 12 unbounded values roughly centered around 0.
    - Vector Breakdown: 
      - 1st dimension represents avg loudness of the segment
      - 2nd emphasizes brightness
      - 3rd correlated with the flatness of the sound
      - 4th to sounds with a stronger attack
      - etc etc
   - Best used in comparison with each other.
     - i.e., if there's a lot of repetetive values b/w sections, you could gather that the song itself is quite repetitive.
   - The timbre features themselves have been PCA'd into the 12 most important features (see above).

