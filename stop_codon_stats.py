"""Given a large fasta file, grab first N sequences
For every sequence, perform a six-frame translation
For every frame, count number of stop codons
Produce descriptive stats for the number of stop codons
"""

import argparse
import fastaparse


