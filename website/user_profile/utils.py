from difflib import SequenceMatcher


class ProfileMatcher:
    """
    A ProfileMatcher object contains the query and ratio_threshold
    """

    def __init__(self, query: str, ratio_threshold=0.36):
        """
        :param query: The keyword to be searched (str)
        :param ratio_threshold: The threshold ratio (float)
        :type query: str
        :type ratio_threshold: float
        """
        self.query = str(query).lower()
        self.ratio_threshold = ratio_threshold

    def matcher(self, obj):
        score = max(
            SequenceMatcher(None, obj.name.lower(), self.query).ratio(),
            -1
        )
        if score >= self.ratio_threshold:
            return score
        return 0

    def __str__(self):
        return 'ProfileMatcher object with query="{}", ratio_threshold={} .'.format(self.query,self.ratio_threshold)
