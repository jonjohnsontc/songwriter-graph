# HookFinder

## Problem Statement
> Develop a model, which given a recording, will recommend similar choruses to the one contained within the song.

## How?
The inspiration for this came from a writeup in Medium that I found from [Vivek Jayaram](https://towardsdatascience.com/finding-choruses-in-songs-with-python-a925165f94a8). In it, he proposes a way to detect a hook in a song based off of locating repeated sections and measuring the gaps between them.

My thought is that I can a) find the "most likely" chorus, given the shape of the sections of songs defined within Spotify's Audio Analysis on each song derived from their API, and then b) use cosine similarity to define the most similar choruses.

