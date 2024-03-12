
# Algorithm: Quick matching of non-overlapping substrings

This repo contains a reference algorithm for a new algorithm designed
by David Broman in 2024 that matches non-overlapping substrings within
a string. The algorithm has O(n log n) time complexity. The limiting factor is standard string sorting, which means the complexity can be improved to run in linear time if linear time sorting is used.

## Introduction

The overall problem may informally be stated as follows:

**Problem:** Given an input string `s`, find the set `A` of all non-overlapping substrings of `s`, giving prioritization over longer matches.

### Input and Output Examples

Suppose we have an input string "banana". In these examples, the symbols are ASCII characters; the actual symbols can be of any type. The task is then to find the set of longest matching substrings. The substring "an" can be found twice, and so do "na". This means that any of these answers are correct. However, only one of the alternatives is valid simultaneously since the substrings "an" and "na" overlap.

If instead the input string is "named banana ban", both "an" and "na" are valid repeats, where both are repeated three times, respectively. However, in this case we have *longer* matches: "ban" is repeated two times: "named **ban**ana **ban**". Hence, we would like the algorithm to report the longest match "ban" (2 times) *and* the rest of the matches that *do not overlap* with the longest match. In this case "an" overaps with `ban` such that there is just one instance of `an` that is not part of the "ban", as follows "named ban**an**a ban" . However, we have two "na" that do not overlap with "ban". That is: "**na**med bana**na** ban".

Hence, in this case, the algorithm should report (i) that "ban" occurs two times, and "na" two times (non-overlapping), and (ii) at which indices these substrings occur.

## The Algorithm and its Reference Implementation

In this repo, we provide a reference implementation in Python. The algorithm consists of 4 steps (see function `matching_substrings` in file `matching-substring.py`:

1. **Suffix array and LCP array construction.** The first step of the algorithm is to construct a [suffix array](https://en.wikipedia.org/wiki/Suffix_array) and the associated [longest common prefix (LCP)](https://en.wikipedia.org/wiki/LCP_array) array. Algorithms exist to construct both these arrays at O(n) time. In the reference implementation, we simply use a standard library `divsufsort` for constructing the suffix array, and [Kasai's algorithm](https://link.springer.com/chapter/10.1007/3-540-48194-X_17) for constructing the LCP array.

2. **Construct tuple list.** This is a preparation step that constructs an array of 3-tuples (called `a` in the implementation `a`), where each 3-tuple contains the following elements: `(l, m, k)`, where
   * `l` = length of the set of equal strings
   * `m` = a marker that identifies each set that is equal
   * `k` = the start index of the position in the string

   In the implementation, note that the length of 'l' is inverted (size of string minus l) to enable correct lexical sorting (max length, lowest index). Intuitively, we iterate through the suffix array and identify matching strings, saving the length `l` in the tuple. The marker `m` is used to identify each set that is equal (there might be several different strings that match with the same length). Finally, the index `k` is stored in the tuple, such that we can easily construct the matching strings afterward. The second step runs in O(n) time.

3. **Sorting of tuple list.** The next step lexically sorts the tuple list that was constructed in step 2. Specifically, the sorting is done in increasing order, such that the indices are sorted in increasing order and that the longest matches come first in the sorted list (recall the inverted length of `l`). This step runs in O(n log n) or O(n) depending on the sorting algorithm.

4. **Construct non-overlapping matching intervals.** The final step uses the sorted tuple list to construct the overlapping indices. There are several important aspects in this step. By using the ordered lists, we prioritize the longest match. As part of this step, the algorithm also uses an array with flags to ensure that we find substrings that do not overlap with previously discovered matching strings. We check this flag before adding a new range. Note that since we always check the longest strings first (marked in the flag array if committed), it is enough to check the start and end of a new substring to know if there is an overlap. Because of these unique treatments of non-overlapping handling, this step runs in O(n) time.

## A First Running Example

Consider again the example "banana". If you run the Python reference example (enable `str1` for this example, which is the default), you get the following output:

```
string:  banana
length:  6
sarray:  [5 3 1 0 4 2]
lcp:     [1 3 0 0 2 0]

Index Match String
5     1     a
3     3     ana
1     0     anana
0     0     banana
4     2     na
2     0     nana

Non-overlapping substring ranges:
Start End   Length SubString
1     3     2      an
3     5     2      an
------------------------------

```
The first lines state that the input string is "banana", and that the length of the input string is 6. Moreover, it prints out the suffix array (`sarray`) and the LCP.

The next lines show the suffix array and the number of matches of characters, which is just another print output from the suffix array and the LCP. For instance, at index 3, we see that there are 3 symbols matching. This means that matching is at index 3 ("ban**ana**") and at the next occurrence in the suffix array, that is at index 1 ("b**ana**na"). Note, however, that these two substrings **are overlapping**. This is also the key problem for the algorithm, i.e., how to find the non-overlapping string.

At the end of the output, we see the result of the matching algorithm. It reports that it found 2 occurrences of "an" (two lines of input), one starting at index 1, and one at index 3. They are guaranteed not to overlap.

## A Second Example

Consider now the longer input "named banana ban" (enable string `str2` in the implementation):

```
string:  named banana ban
length:  16
sarray:  [12  5 11  1 14  9  7 13  6  4  3  2 15 10  0  8]
lcp:     [4 0 1 1 2 3 0 3 0 0 0 0 1 2 2 0]

Index Match String
12    4      ban
5     0      banana ban
11    1     a ban
1     1     amed banana ban
14    2     an
9     3     ana ban
7     0     anana ban
13    3     ban
6     0     banana ban
4     0     d banana ban
3     0     ed banana ban
2     0     med banana ban
15    1     n
10    2     na ban
0     2     named banana ban
8     0     nana ban

Non-overlapping substring ranges:
Start End   Length SubString
5     9     4       ban
12    16    4       ban
------------------------------
0     2     2      na
10    12    2      na
------------------------------
```

We can now see that the algorithm produces two output sets, one for the matching of "ban" (two occurrences), and one for "na" (two occurrences)". In this case, the algorithm matched in total these substrings, marked in bold: "**na**med **ban**a**na** **ban**"

Please see the reference implementation for details. There are several test cases that can be tried out by changing the value of variable `test_string`.

# Limitations

This algorithm finds the longest non-overlapping substrings and often finds shorter matches as well, although there is no guarantee of finding all shorter matches.

# Acknowledgements

Big thanks to Rohan Yadav for discussing the algorithm and for introducing
the problem (within the domain of distributed computing), which
triggered the design of the algorithm.
