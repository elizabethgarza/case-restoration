#!/usr/bin/env python3
"""Utility functions."""


from typing import Iterator, List


def sentences_from_file(filename: str) -> Iterator[List[str]]:
    with open(filename, "r") as source: 
        for line in source:
            yield line.split()


def tokens_from_file(filename: str) -> Iterator[str]:
    for sentence in sentences_from_file(filename):
        yield from sentence