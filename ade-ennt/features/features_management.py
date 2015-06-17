"""
    Manages the features extraction and merge
"""

import features.adrs as adrs
import features.descriptors as descriptors


FEATURES = {
    'adrs1': adrs.generate(level=1),
    'adrs2': adrs.generate(level=2),
    'adrs3': adrs.generate(level=3),
    'adrs4': adrs.generate(level=4),
    'descriptors': descriptors.generate
}

def get_feature(feature_nr):
    """ Retrieves the selected feature """

    return FEATURES[feature_nr]()


def get_merged_features(ftrs):
    """ Retrieves the selected features, merged by id """

    result_df = get_feature(ftrs[0])()

    for ftr in FEATURES[1:]:
        result_df = result_df.join(get_feature(ftr), how='inner')

    return result_df
