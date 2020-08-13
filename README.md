adapted from Kyle Gorman, Emily Campbell, and Elizabeth Garza's README.md from `CUNYCL/WinterCamp`

# Purpose

The purpose of this experiment is to 
- restore missing capitalization in noisy user-generated text as is often found in text messages (SMS) or posts on social media, or even
- add capitalization to the output of machine translation and speech recognition to make them easier for humans to read, or even
- transfer the "style" of casing from one collection of documents to another.

# Background information on case restoration

Nearly all speech and language technologies work by collecting statistics over huge collections of characters and/or words. While handful of words (like the or she) are very frequent, the vast majority of words (like ficus or cephalic) are quite rare. One of the major challenges in speech and language technology is making informed predictions about the linguistic behaviors of rare words.

Many writing systems, including all of those derived from the Greek, Latin, and Cyrillic alphabets, distinguish between upper- and lower-case words. Such writing systems are said to be bicameral, and those which do not make these distinctions are said to be unicameral. While casing can carry important semantic information (compare bush vs. Bush), this distinction also can introduce further "sparsity" to our data. Or as Church (1995) puts it, do we really need to keep totally separate statistics for hurricane or Hurricane, or can we merge them?

In most cases, speech and language processing systems, including machine translation and speech recognition engines, choose to ignore casing distinctions; they casefold the data before training. While this is fine for many applications, it is often desirable to restore capitalization information afterwards, particularly if the text will be consumed by humans.

Lita et al. (2003) introduce a task they call "true-casing". They use a simple machine learning model, a hidden Markov model, to predict the capitalization patterns of sentences, word by word. They obtain good overall accuracy (well about 90% accurate) when applying this method to English news text.


  
