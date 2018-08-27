import random
import string
from nltk.tag import pos_tag
#from itertools import compress

#def remove_special_char(st):
#       t = str.maketrans(',','""')
#       st.translate(t)
#       return st

def find_punct(st):
    """
    Returns list of tuples with the location corresponding punctuation for items in string
    """
    #loc = [c in string.punctuation for c in st]
    loc = [n for n in range(len(st)) if st[n] in string.punctuation]
    if len(loc) == 0:
        return []
    else:
        punct = [st[n] for n in range(len(st)) if st[n] in string.punctuation]
        return zip(loc,punct)

def remove_punct(st):
    """
    Returns string identical to the string passed in except with punctuation removed
    """
    if len(st) > 1:
        _ = find_punct(st)
        if _:
            punct = zip(*_)
            l = next(punct)
            all_chars = set(range(len(st)))
            return  ''.join([st[c] for c in all_chars - set(l)])
        else:
            return st
    else:
        return st

def restore_punct(st_np, st_orig):
    """
    This takes two strings. The first arguments should be a string where you want punctuation to be injected. The second string is a string with punctuation. The punctuation in the second string will be added to the corresponding location in the first string
    """
    l_np = list(st_np)
    n=0
    for c in st_orig:
        if c in string.punctuation:
            l_np.insert(n, c)
        n += 1
    return ''.join(l_np)

def shuffle_string(st):
    l = list(st)
    random.shuffle(l)
    return(''.join(l))

def partially_shuffle_string(st):
    """
    Shuffles a string except for the first and last character
    """
    if all(x == st[1] for x in st[1:-1]):
        return st
    if len(st) > 2:
        shuff = st[1:-1]
        while(shuff == st[1:-1]):
            shuff = shuffle_string(st[1:-1])
            tmp = st[0] + shuff + st[-1]
    else:
        tmp = st
    return ''.join(tmp)

def wordscram(txtfile):
    """
    The input is the full path to a text file. Returns a scrambled version of the textfile as a string with the characters scrambled
    except for the first and last letters of each word and for punctuation, and proper nouns
    """
    f = open(txtfile, encoding='utf-8')
    txt = list(f)
    f.close()

    wds = []
    for l in txt:
        wds.append([w for w in l.split(' ')])

    wds_nr = []
    for l in wds:
      wds_nr.append([w.rstrip() for w in l])

    # flatten list
    wds_flat = []
    for l in wds_nr:
        for w in l:
            wds_flat.append(w)

    # create punctuation free version of the list of words
    wds_no_punct = [remove_punct(w) for w in wds_flat]

    # alter words
    wds_alt = [partially_shuffle_string(w) for w in wds_no_punct]

    # restore proper nouns
    tagged_wds = pos_tag(wds_no_punct)
    tagged_wds = list(zip(*tagged_wds))
    _ = list(zip(wds_no_punct,wds_alt,tagged_wds[1]))
    wds_alt_proper_nouns = []
    for wd in _:
        if wd[2] == 'NNP':
            wds_alt_proper_nouns.append(wd[0])
        else:
            wds_alt_proper_nouns.append(wd[1])


    wds_alt = wds_alt_proper_nouns

    # restore punctuation
    wds_scram = [restore_punct(wds_alt[cnt], wds_flat[cnt]) for cnt in range(len(wds_alt))]

    return ' '.join(wds_scram)

if __name__ == '__main__':
    import sys
    out = wordscram(sys.argv[1])
    print(out)
