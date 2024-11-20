# Sample viral genome (simplified for demonstration)
viral_genome = "GAATTCATGCGCGCGCTAGCATCGATCGATCGAATTCGCTAGCATCGATCGAGCTAGCATCG"

# Dictionary of restriction enzymes and their recognition sequences
restriction_enzymes = {
    'EcoRI': 'GAATTC',
    'NheI': 'GCTAGC'
}

def digest_dna(sequence, enzymes):
    """
    Digest DNA sequence with given restriction enzymes
    Returns list of tuples: (fragment, start_pos, end_pos, gc_content)
    """
    # Find all cut sites
    cut_sites = []
    for enzyme, recognition_seq in enzymes.items():
        pos = 0
        while True:
            pos = sequence.find(recognition_seq, pos)
            if pos == -1:
                break
            cut_sites.append(pos)
            pos += 1
    
    # Add start and end positions
    cut_sites = sorted([0] + cut_sites + [len(sequence)])
    
    # Generate fragments
    fragments = []
    for i in range(len(cut_sites) - 1):
        start = cut_sites[i]
        end = cut_sites[i + 1]
        fragment = sequence[start:end]
        
        # Calculate GC content
        gc_count = fragment.count('G') + fragment.count('C')
        gc_content = gc_count / len(fragment) if fragment else 0
        
        fragments.append((fragment, start, end, gc_content))
    
    return fragments