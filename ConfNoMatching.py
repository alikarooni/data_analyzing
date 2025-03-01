import string_comparison as SC
from typing import List

class MatchLevel:
    IsMatch = 10
    MaybeMatch = 20
    NoMatch = 30
    NotFound = 40

class ConfNoComparator:
    def __init__(
        self,
        required_length=3,
        min_num_of_numerics_when_length_more_than_ten=4,
        min_num_of_numerics_when_length_equal_six=5,
        section_separators=None
    ):
        self.RequiredLength = required_length
        self.MinNumOfNumericsWhenLengthMoreThanTen = min_num_of_numerics_when_length_more_than_ten
        self.MinNumOfNumericsWhenLengthEqualSix = min_num_of_numerics_when_length_equal_six
        self.SectionSeparators = section_separators or "||"
    
    def Compare(self, confNo1, confNo2):
        # Missing ConfNo
        # if confNo1 is None or confNo2 is None or not confNo1.strip() or not confNo2.strip():
        #     return MatchLevel.NoMatch

        # Split to sections and remove empties
        sectionsConfNo1 = [s.strip() for s in confNo1.split(self.SectionSeparators) if s.strip()]
        sectionsConfNo2 = [s.strip() for s in confNo2.split(self.SectionSeparators) if s.strip()]
        
        # Only empty sections
        if len(sectionsConfNo1)==0 or len(sectionsConfNo2)==0:
            return MatchLevel.NotFound

        # Compare sections from first and second ConfNo
        sectionMatchLevels = [self.CompareSections(sectionConfNo1, sectionConfNo2) for sectionConfNo1 in sectionsConfNo1 for sectionConfNo2 in sectionsConfNo2]
        
        # Determine match level
        if MatchLevel.IsMatch in sectionMatchLevels:
            return MatchLevel.IsMatch
        elif MatchLevel.MaybeMatch in sectionMatchLevels:
            return MatchLevel.MaybeMatch
        else:
            return MatchLevel.NoMatch

    def CompareMultiple(
        self,
        candidate_conf_no: str,
        candidate_conf_no_list: List[str],
        compare_conf_no: str,
        compare_conf_no_list: List[str],
    ) -> MatchLevel:
        results = [self.Compare(candidate_conf_no, compare_conf_no)]
        if results[0] == MatchLevel.IsMatch:
            return results[0]

        for cn in candidate_conf_no_list:
            for ccn in compare_conf_no_list:
                results.append(self.Compare(cn, ccn))
        
        results.sort()
        return results[0]

    def CompareSections(self, sectionConfNo1, sectionConfNo2):
        # Determine shorter and longer
        if len(sectionConfNo1) > len(sectionConfNo2):
            shorter = sectionConfNo2
            longer = sectionConfNo1
        else:
            shorter = sectionConfNo1
            longer = sectionConfNo2

        # Find longest common substring
        lcs = SC.LCS(shorter, longer)
        
        # Compare ConfNo        
        if self.IsMatch(shorter, longer, lcs):
            return MatchLevel.IsMatch
        elif self.IsMaybeMatch(shorter, longer, lcs):
            return MatchLevel.MaybeMatch
        else:
            return MatchLevel.NoMatch

    def IsMatch(self, shorter, longer, lcs):
        # Helpers
        numOfNumericsInShorter = self.NoOfNumerics(shorter)
        shorterLength = len(shorter)
        
        # At least MinNumOfNumerics and sub
        if (sum([1 for i in shorter[1:] if i==shorter[0]])==(len(shorter)-1) or
            sum([1 for i in longer[1:] if i==longer[0]])==(len(longer)-1)):
            return False

        currenttime = ''
        if(currenttime > '2023-01-26'):
            if(numOfNumericsInShorter >= self.MinNumOfNumericsWhenLengthMoreThanTen and shorter in longer):
                return True
        else:
            if ((numOfNumericsInShorter >= self.MinNumOfNumericsWhenLengthMoreThanTen and shorterLength >= 10) or
                    (numOfNumericsInShorter >= self.MinNumOfNumericsWhenLengthEqualSix and shorterLength == 6) and shorter in longer):
                return True

        # Longest common substring match
        if self.IsLongestCommonSubstringMatch(shorter, longer, lcs):
            return True

        # Otherwise it is not a match
        return False

    def IsLongestCommonSubstringMatch(self, shorter, longer, lcs):
        # Helpers
        lcsNumOfNumerics = self.NoOfNumerics(lcs)

        # Longest common string with at least MinNumOfNumerics
        # All numerics included from both sides
        return lcsNumOfNumerics >= self.MinNumOfNumericsWhenLengthMoreThanTen and \
               lcsNumOfNumerics == self.NoOfNumerics(shorter) and \
               lcsNumOfNumerics == self.NoOfNumerics(longer)

    def IsMaybeMatch(self, shorter, longer, lcs):
        # At least RequiredLength
        if len(shorter) < self.RequiredLength:
            return False

        if (sum([1 for i in shorter[1:] if i==shorter[0]])==(len(shorter)-1) or
            sum([1 for i in longer[1:] if i==longer[0]])==(len(longer)-1)):
            return False

        # NUM, LETTER, MIX
        # if (type(a) != type(b)) return false
        # Both PNR and sub
        if self.IsSubOrPnrMatch(shorter, longer, lcs):
            return False

        # At most 1 difference of 5 characters
        distance = self.compute_levenshtein(shorter, longer)
        return distance >= 0.85, len(xx)>=7

    def IsSubOrPnrMatch(self, shorter, longer, lcs):
        # Helpers
        lcsNumOfNumerics = self.NoOfNumerics(lcs)
        length = len(lcs)
        noOfLetters = self.NoOfLetters(lcs)
        noOfNumerics = self.NoOfNumerics(lcs)

        # At least 6 characters (PNR is 6 characters but allow matching noise)
        # Only letters and numerics
        # At least one letter
        # At least one numeric
        return length == 6 and noOfLetters + noOfNumerics == length and noOfLetters >= 1 and noOfNumerics >= 1

    def NoOfNumerics(self, s):
        return sum(c.isdigit() for c in s)

    def NoOfLetters(self, s):
        return sum(c.isalpha() for c in s)
    
    def compute_distance(self, str1, str2, add=1, delete=1, substitute=1):
        return self.compute_distance_helper(list(str1), list(str2), add, delete, substitute)

    def compute_distance_helper(self, str1, str2, insert, delete, substitute):
        distance = [[0 for j in range(len(str2) + 1)] for i in range(len(str1) + 1)]

        for i in range(len(str1) + 1):
            distance[i][0] = i * delete

        for j in range(len(str2) + 1):
            distance[0][j] = j * insert

        for i in range(1, len(str1) + 1):
            for j in range(1, len(str2) + 1):
                distance[i][j] = self.minimum(
                    distance[i - 1][j] + delete,
                    distance[i][j - 1] + insert,
                    distance[i - 1][j - 1] + (0 if str1[i - 1] == str2[j - 1] else substitute)
                )

        return distance[len(str1)][len(str2)]

    def minimum(self, a, b, c):
        if a <= b and a <= c:
            return a
        if b <= a and b <= c:
            return b
        return c
    
    def compute_levenshtein(self, s1, s2):
        t1 = (s1 or "").strip()
        t2 = (s2 or "").strip()
        if len(t1) == 0 or len(t2) == 0:
            return 0

        # Calculate distance
        distance = self.compute_distance(t1, t2)

        # Calculate similarity
        # Maximum difference is string length (all different characters)
        similarity = 1.0 - (float(distance) / max(len(t1), len(t2)))

        # Return similarity scaled to [0..1]
        return similarity