def get_sec_means(mean_dicts):
    '''
    Create df out of section means in `mean_dicts`.
    '''
    section_mean = pd.DataFrame(columns=['confidence', 'duration', 'loudness', 'mode',
                                        'mode_confidence', 'tempo', 'tempo_confidence'])

    for e in mean_dicts:
        section_mean.loc[list(e.keys())[0]] = list(e.values())[0]
    return section_mean