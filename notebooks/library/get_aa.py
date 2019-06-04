# Put this with all of the other Spotify related access functions

import json
import time

def get_aa(song_list):
    '''
    Retrieve audio analysis for every song in `song_list` and store each in separate .json file.
    '''
    count = 0
    for i in song_list:
        if isinstance(i, dict):
            for k in i['tracks']:
                try:
                    analysis = sp.audio_analysis(k['id'])
                except:
                    time.sleep(5)
                    analysis = sp.audio_analysis(k['id'])
                with open('../data/audio_analysis/{}.json'.format(k['id']), 'w') as f:
                    json.dump(analysis, f)
        count += 1
        if count % 5000 == 0:
            print('song {} finished'.format(count))
    print('finished')