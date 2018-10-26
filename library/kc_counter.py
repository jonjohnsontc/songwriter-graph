def kc_counter(lst):
    '''
    Return count of key changes throughout songs listed in individual json files
    lst = refers to .json song listing
    '''
    kc_list = []
    for record in lst:
        with open('../data/audio_analysis/{}'.format(record), 'r') as f:
            analysis = json.load(f)
            if isinstance(analysis, dict):
                if 'sections' in analysis:
                    try:
                        start_key = analysis['sections'][0]['key']
                        kc = 0
                        for item in analysis['sections']:
                            cur_key = item['key']
                            if cur_key != start_key:
                                start_key = cur_key
                                kc += 1
                        kc_list.append(dict({record.replace('.json', ''):kc}))
                    except:
                        kc_list.append(dict({record.replace('.json', ''): 'unable to record key changes'}))
    return kc_list