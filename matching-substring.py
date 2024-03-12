# Algorithm: Compute matching non-overlapping substrings.
#            Time complexity O(n log n) using standard sorting
# The algorithm was invented and implemented by David Broman in 2024
#
# Note: please install Python package 'pydivsufsort'

from pydivsufsort import divsufsort, kasai

# Test function for printing the suffix array and
# LCP, together with a table with all sorted matching strings.
def print_sarray_lcp(str, sarray, lcp):
    print("string: ", str)
    print("length: ", len(str))
    print("sarray: ", sarray)
    print("lcp:    ", lcp)
    print("\nIndex Match String")
    for i in range(len(str)):
        sr = sarray[i]
        (e, s) = (len(str), "") if len(str) - sr < 50 else (sr + 50, "...")
        print(f"{sarray[i]:<5} {lcp[i]:<5} {str[sarray[i]:e]}{s}")

# Test function for pretty printing the non-overlapping intervals
def print_string_intervals(str, t):
    print("\nNon-overlapping substring ranges:")
    print("Start End   Length SubString")
    for r in t:
        for (s, e) in r:
            print(f"{s:<5} {e:<5} {e-s:<6} {str[s:e]}")
        print("------------------------------")

# The main matching function for computing non-overlapping
# matching substrings.
#
# Input:
# It takes the string 'str' as input,
# together with constraints of the minimum length of wanted strings
# ('min_str'), maximum length ('max_str') and the minimal number of
# repetitions that are allowed ('min_rep').
#
# Output:
# As output, it generates a list of lists, where each inner list
# element consists of a lists of ranges of matching strings. Each
# match is encoded as a tuple, with the start and end index.
def matching_substrings(str, min_str, max_str, min_rep):

    ### Step 1: Compute suffix array and longest common prefix: O(n log n)
    #           Note that there exist O(n) variants in the literature.
    sarray = divsufsort(str)
    lcp = kasai(str, sarray);

    ### Step 2: Construct tuple list: O(n)
    a, m, pre_l = [], 0, 0
    for i, l1 in enumerate(lcp):
        if i+1 < len(lcp):
            s1, s2 = sarray[i], sarray[i+1]
            le = len(str)
            if s2 >= s1 + l1 or s2 <= s1 - l1:
                # Non-overlapping
                if pre_l != l1:
                    m += 1
                a.append((le - l1, m, s1))
                a.append((le - l1, m, s2))
                pre_l = l1
            elif s2 > s1 and s2 < s1 + l1:
                # Overlapping, increasing index
                d = s2 - s1
                l3 = (((l1 + d) // 2) // d) * d
                if pre_l != l3:
                    m += 1
                a.append((le - l3, m, s1))
                a.append((le - l3, m, s1 + l3))
                pre_l = l3
            elif s1 > s2 and s1 < s2 + l1:
                # Overlapping, decreasing index
                d = s1 - s2
                l3 = (((l1 + d) // 2) // d) * d
                if pre_l != l3:
                    m += 1
                a.append((le - l3, m, s2))
                a.append((le - l3, m, s2 + l3))
                pre_l = l3

    ### Step 3: Sorting of tuple list: O(n log n)
    a_sorted = sorted(a)

    ### Step 4: Construct matching intervals: O(n)
    r, t, m_pre, next_k = [], [], 0,  0
    flag = [False] * len(str)
    for (l, m, k) in a_sorted:
        le = len(str) - l
        if m != m_pre:
            if len(r) >= min_rep:
                t.append(r)
                for (k1, k2) in r:
                    for j in range(k1, k2):
                        flag[j] = True
            r = []
            next_k = 0
        m_pre = m
        if le != 0 and le >= min_str and le <= max_str and k >= next_k \
           and not(flag[k]) and not(flag[k + le -1]):
            r.append((k, k + le))
            next_k = k + le
    if len(r) >= min_rep:
        t.append(r)
    return t


str1 = "banana"
str2 = "named banana ban"
str3 = "aaabbbaaabbb"
str4 = "abcabcdefabcabcdef"
str5 = "aaaaaaabbbbccccccc"
str6 = "ababababababcdcdcdcd"
str7 = "ababaab_abababab"
str8 = "aaaaaaabbbbbbaaaaaa"
str9 = "aaaaaabaa"
str10 = "fsi12-fgwo918nsa...fgwo918nsa!fgwo918nsa+1+fgwo918nsa???"

str11 = "aaaac"
str12 = "aaaaaaaaaac"
str13 = "ababc"
str14 = "abababc"
str15 = "ababac"
str16 = "ababababc"

str21 = "aaaa"
str22 = "aaaaa"
str23 = "abab"
str24 = "ababab"
str25 = "ababa"
str26 = "abababab"
str27 = "aaaaaa"
str28 = "aaa"

str30 = "aaaabbbb"
str31 = "aaaaabbbbb"
str32 = "ababcdcdcd"
str33 = "abababcdcdcd"
str34 = "3188318"
str35 = "bfdddababcdcdcdeddd"

str40 = "aaaabbbbaaaabbbbc"
str41 = "aaaabbbbaaaabbbbaaaabbbbaaaabbbbac"
str42 = "aaaabbbbaaaabbbb"
str43 = "12aaaabbbbaaaabbbbaaaabbbbaaaabbbb12"

str50 = "This is just a test string with some more testing. Let's see what"\
        "finds in this string."
str51 = "Test a long string"*20

# --- Perform test experiments here --- **********************
test_string = str1
min_substr_len = 2
max_substr_len = 500
min_no_repeats = 2
# ------------------------------------- **********************

# Main test program: prints the suffix array, prints the LCP,
# executes the new algorithm, and prints the intervals in readable format.
sarray = divsufsort(test_string)
lcp = kasai(test_string, sarray);
print_sarray_lcp(test_string, sarray, lcp)
t = matching_substrings(test_string, min_substr_len, max_substr_len,
                        min_no_repeats)
print_string_intervals(test_string, t)


