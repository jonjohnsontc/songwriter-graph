def get_sec_var(var_dicts):
    '''
    Create df out of section variances in `var_dicts`.
    '''
    section_var = pd.DataFrame(columns=['confidence', 'duration', 'loudness', 'mode',
                                        'mode_confidence', 'tempo', 'tempo_confidence'])

    for e in var_dicts:
        section_var.loc[list(e.keys())[0]] = list(e.values())[0]
    return section_var