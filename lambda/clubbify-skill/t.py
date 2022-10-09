def filterString(iString):
        # declare variable to hold filler words
        fillerWords = ['oh', 'um', 'uh', 'er', 'ah', 'like', 'well', 'so', 'right', 'literally', 'okay']
        
        # first get rid of all duplicates
        r = set(iString.split())
        
        # go through the set and remove any filler words
        for i in range(len(r)):
            if r[i] in fillerWords:
                r.remove(r[i])
        # return the set
        return r