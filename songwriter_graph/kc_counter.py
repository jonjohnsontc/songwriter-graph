import json

def kc_counter(lst, fp):
    '''
    Return count of key changes throughout songs listed in individual json files
    fp = refers to the file path for the song files
    lst = refers to .json song listing
    '''
    kc_list = {}
    errors = {}
    count = 0
    for record in lst:
        count += 1
        try:
            with open(f'{fp}/{record}.json', 'r') as f:
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
                        kc_list[record.replace('.json', '')] = kc
                    except Exception as e:
                        kc_list[record.replace('.json', '')] = f'{e} unable to record key changes'
        except Exception as e:
            errors[record] = e
        if count % 25000 == 0:
            print(f'{count} songs attempted')
    return kc_list, errors