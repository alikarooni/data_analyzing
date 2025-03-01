import numpy as np
import re
import jellyfish


def Jaro_Winkler(str1, str2):
    return jellyfish.jaro_winkler(str1, str2)

def damerau_levenshtein_distance(s1, s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1
    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,  # deletion
                d[(i, j - 1)] + 1,  # insertion
                d[(i - 1, j - 1)] + cost,  # substitution
            )
            if i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[(i - 2, j - 2)] + cost)  # transposition
    return d[(lenstr1 - 1, lenstr2 - 1)]

def jaccard_similarity(str1, str2):
    set1 = set(str1)
    set2 = set(str2)
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return 0 if(len(union)==0) else len(intersection) / len(union) 

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def create_vector(string1, string2, separator):
    # Preprocess and split the strings into words
    words1 = string1.split(separator)
    words2 = string2.split(separator)
    
    # Create a set of all words in both strings
    all_words = set(words1 + words2)
    
    # Create a vector for each string with the frequency of each word
    vector1 = np.zeros(len(all_words))
    vector2 = np.zeros(len(all_words))
    for i, word in enumerate(all_words):
        if word in words1:
            vector1[i] = words1.count(word)
        if word in words2:
            vector2[i] = words2.count(word)
    
    return vector1, vector2

def LCS(X, Y):
    m = len(X)
    n = len(Y)
    L = [[None]*(n+1) for i in range(m+1)]

    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1] + 1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])

    index = L[m][n]
    lcs = [""] * (index+1)
    lcs[index] = ""

    i = m
    j = n
    while i > 0 and j > 0:
        if X[i-1] == Y[j-1]:
            lcs[index-1] = X[i-1]
            i -= 1
            j -= 1
            index -= 1
        elif L[i-1][j] > L[i][j-1]:
            i -= 1
        else:
            j -= 1
    return "".join(lcs)


def get_other_chars(str):
    pattern = r"[^0-9a-zA-Z1-9]"
    matches = set(re.findall(pattern, str))
    return ''.join(matches)

def no_digits(str):
    pattern = r"\d"
    return len(re.findall(pattern, str))

def no_alphas(str):
    pattern = r"[a-zA-Z]+"
    return len(''.join(re.findall(pattern, str)))

def get_alphas(str):
    pattern = r"[a-zA-Z]+"
    return ''.join(re.findall(pattern, str))

def get_TR_stats(str):
    res = {'numalpha_type':'', 'no_nums':0, 'no_alphas':0, 'no_others':0, 'otherchars':''}

    if(str.lower() == 'nan'):
        res['numalpha_type'] = 'NAN'
        res['no_nums'] = 0
        res['no_alphas'] = 0
        res['no_others'] = 0
    elif(str.isdigit()):
        res['numalpha_type'] = 'NUM'
        res['no_nums'] = len(str)
    elif(str.isalpha()):
        res['numalpha_type'] = 'ALPHA'
        res['no_alphas'] = len(str)
    elif(str.isalpha()==False and str.isdigit()==False):
        otherchars = get_other_chars(str)
        if(len(otherchars) == 0):
            res['numalpha_type'] = 'NUMALPHA'
            res['no_nums'] = no_digits(str)
            res['no_alphas'] = no_alphas(str)
        else:
            res['numalpha_type'] = 'OTHER'
            res['no_nums'] = no_digits(str)
            res['no_alphas'] = no_alphas(str)
            res['no_others'] = len(otherchars)
            res['otherchars'] = otherchars
    return res

def remove_special_chars(text):
    special_chars = ['~','`','!','@','#','$','%','^','&','*','(',')','','_','-','=',
     '+','[',']','{','}',';',':',"'",'"','\\','|', '/', '?','.','<','>','.',
     ',','Ï', '¿', '½', '', '™', ' ']
    for s in special_chars:
        text = text.replace(s, '')
    return text

def dict_sort(d):
    new_dict = {}
    keys = sorted(list(d.keys()))
    for k in keys:
        new_dict[k] = d[k]
    return new_dict

def get_special_chars(text):
    special_chars = ['~','`','!','@','#','$','%','^','&','*','(',')','','_','-','=',
     '+','[',']','{','}',';',':',"'",'"','\\','|', '/', '?','.','<','>','.',
     ',','Ï', '¿', '½', '', '™', ' ']

    res = set()
    for t in text:
        if(t in special_chars):
            res.add(t)
    return res