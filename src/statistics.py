#!/usr/bin/env python3
"""Case restoration summary statistics."""

import argparse
import collections
import logging
import os

import case
import util

def main(args):

    os.chdir('..')
    os.chdir('data')

    # Collects counts.
    case_counts = collections.Counter()
    token_to_case_set = collections.defaultdict(set)
    token_to_pattern_set = collections.defaultdict(set)
    for (i, token) in enumerate(util.tokens_from_file(args.file_path), 1):
        if i % 1_000_000 == 0:
            logging.info("%d tokens read", i)
        (tc, pattern) = case.get_tc(token)
        token = token.casefold()
        case_counts[tc] += 1
        token_to_case_set[token].add(tc)
        if pattern:  # I.e., is mixed-case.
            # Converts to tuple to make it hashable.
            token_to_pattern_set[token].add(tuple(pattern))
    # Logs results.
    z = sum(case_counts.values())
    print(f"Data size:\t{z:,}")
    # Count by case.
    for (tc, count) in case_counts.most_common():
        print(f"{tc.name}\t{count / z:.4f}\t{count:,}")
    # Case-ambiguous tokens.
    ambiguous_tokens = 0
    for token_cases in token_to_case_set.values():
        if len(token_cases) > 1:
            ambiguous_tokens += 1
    print(
        f"Ambiguous tokens:\t"
        f"{ambiguous_tokens / len(token_to_case_set):.4f}\t"
        f"({ambiguous_tokens:,})"
    )
    # Case-ambiguous mixed tokens.
    ambiguous_mixed_tokens = 0
    for patterns in token_to_pattern_set.values():
        if len(patterns) > 1:
            ambiguous_mixed_tokens += 1
    print(
        f"Ambiguous mixed-case tokens:\t"
        f"{ambiguous_mixed_tokens / len(token_to_pattern_set):.4f}\t"
        f"({ambiguous_mixed_tokens})"
    )


if __name__ == "__main__":
    logging.basicConfig(level="INFO", format="%(levelname)s: %(message)s")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file_path", help="Tokenized data")
    main(parser.parse_args())