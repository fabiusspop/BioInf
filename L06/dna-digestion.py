import re
from typing import List, Tuple

# Zika virus partial sequence
viral_genome = """
AGTTGTTGATCTGTGTGAATCAGACTGCGACAGTTCGAGTTTGAAGCGAAAGCTAGCAACAGTATCAACAGGTTTTATTTTGGATTTGGAAACGAG
AGTTTCTGGTCATGAAAAACCCAAAAAAGAAATCCGGAGGATTCCGGATTGTCAATATGCTAAAACGCGGAGTAGCCCGTGTGAGCCCCTTGGGAG
GTTTGAAGAGGCTGCCAGCCGGACTTCTGCTGGGTCATGGGCCCATCAGGATGGTCTTGGCGATTCTAGCCTTTTTGAGATTCACGGCAATCAAGC
"""

# Define restriction enzyme recognition sites (patterns)
restriction_enzymes = {
    'EcoRI': 'GAATTC',    # G and A
    'BamHI': 'GGATCC',    # G and G
    'HindIII': 'AAGCTT',  # A and A
    'NotI': 'GCGGCCGC'    # G and C
}

def clean_sequence(sequence: str) -> str:
    return ''.join(sequence.split())

def calculate_gc_content(sequence: str) -> float:
    gc_count = sequence.count('G') + sequence.count('C')
    return (gc_count / len(sequence)) * 100 if sequence else 0

def find_restriction_sites(sequence: str, pattern: str) -> List[int]:
    """Find all positions where restriction enzyme cuts"""
    return [match.start() for match in re.finditer(pattern, sequence)]

def digest_dna(sequence: str, enzymes: dict) -> List[Tuple[str, int, int, float]]:
    """Digest DNA sequence with given restriction enzymes"""
    sequence = clean_sequence(sequence)
    cut_positions = set()
    
    # cut positions
    for enzyme, pattern in enzymes.items():
        positions = find_restriction_sites(sequence, pattern)
        for pos in positions:
            cut_positions.add(pos)
    
    cut_positions = sorted(list(cut_positions))
    
    # Generating fragments
    fragments = []
    start_pos = 0
    
    for cut_pos in cut_positions:
        fragment = sequence[start_pos:cut_pos]
        if fragment:
            gc_content = calculate_gc_content(fragment)
            fragments.append((fragment, start_pos, cut_pos, gc_content))
        start_pos = cut_pos
    
    # final fragment
    if start_pos < len(sequence):
        final_fragment = sequence[start_pos:]
        gc_content = calculate_gc_content(final_fragment)
        fragments.append((final_fragment, start_pos, len(sequence), gc_content))
    
    return fragments

def main():
    # DNA digestion
    fragments = digest_dna(viral_genome, restriction_enzymes)
    
    print("DNA Digestion Results:")
    print("-" * 80)
    print(f"{'Fragment':<20} {'Length':<10} {'Start':<10} {'End':<10} {'GC Content':<12}")
    print("-" * 80)
    
    for fragment, start, end, gc_content in fragments:
        print(f"{fragment[:17]+'...' if len(fragment)>17 else fragment:<20} "
              f"{len(fragment):<10} "
              f"{start:<10} "
              f"{end:<10} "
              f"{gc_content:.2f}%")

if __name__ == "__main__":
    main()
