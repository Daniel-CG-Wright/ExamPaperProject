# used to specify common exam question criteria.


class CriteriaStruct:

    def __init__(self, topics: set, minmarks: int, maxmarks: int,
                 component: str, level: str,
                 noParts: bool,
                 contentsearch: str = ""):
        """
        Creates a criteria class with topics, minmarks, maxmarks
        etc and an optional contentsearch (for question bank
        use)
        """
        self.topics = topics
        self.minmarks = minmarks
        self.maxmarks = maxmarks
        self.component = component
        self.level = level
        self.noParts = noParts
        self.contentsearch = contentsearch
