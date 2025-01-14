from typing import List, Tuple, Dict
import re

class TransposonDetector:
    def __init__(self, min_ir_length: int = 5, max_ir_length: int = 10):
        self.min_ir_length = min_ir_length
        self.max_ir_length = max_ir_length
        self.transposons = []
    
    def find_inverted_repeats(self, sequence: str) -> List[Dict]:
        """Find all potential inverted repeats in the sequence"""
        ir_pairs = []
        
        # Look for inverted repeats of different lengths
        for ir_length in range(self.min_ir_length, self.max_ir_length + 1):
            for i in range(len(sequence) - ir_length + 1):
                left_ir = sequence[i:i + ir_length]
                # Get reverse complement of left IR
                right_ir = self._reverse_complement(left_ir)
                
                # Look for matching right IR
                j = i + ir_length
                while True:
                    j = sequence.find(right_ir, j)
                    if j == -1:
                        break
                    
                    # Store found IR pair
                    ir_pairs.append({
                        'left_pos': i,
                        'right_pos': j,
                        'left_ir': left_ir,
                        'right_ir': right_ir,
                        'length': j + ir_length - i
                    })
                    j += 1
        
        return ir_pairs
    
    def _reverse_complement(self, seq: str) -> str:
        """Get reverse complement of DNA sequence"""
        complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        return ''.join(complement[base] for base in reversed(seq))
    
    def detect_transposons(self, sequence: str) -> List[Dict]:
        """Detect all transposons in the sequence"""
        # Find all potential IR pairs
        ir_pairs = self.find_inverted_repeats(sequence)
        
        # Filter and organize transposons
        transposons = []
        for ir in ir_pairs:
            transposon = {
                'start': ir['left_pos'],
                'end': ir['right_pos'] + len(ir['right_ir']),
                'left_ir': ir['left_ir'],
                'right_ir': ir['right_ir'],
                'sequence': sequence[ir['left_pos']:ir['right_pos'] + len(ir['right_ir'])]
            }
            transposons.append(transposon)
        
        # Sort by length (longest first) to handle nested transposons
        transposons.sort(key=lambda x: len(x['sequence']), reverse=True)
        
        # Remove redundant and invalid transposons
        filtered_transposons = self._filter_transposons(transposons)
        
        return filtered_transposons
    
    def _filter_transposons(self, transposons: List[Dict]) -> List[Dict]:
        """Filter out invalid and redundant transposons"""
        filtered = []
        for i, transposon in enumerate(transposons):
            # Check minimum length
            if len(transposon['sequence']) < 20:  # Minimum reasonable length
                continue
                
            # Check if this transposon is valid
            is_valid = True
            for existing in filtered:
                # Check for complete overlap (nested)
                if (transposon['start'] >= existing['start'] and 
                    transposon['end'] <= existing['end']):
                    is_valid = False
                    break
                
                # Check for significant overlap
                overlap = min(transposon['end'], existing['end']) - \
                         max(transposon['start'], existing['start'])
                if overlap > 0 and overlap > 0.5 * len(transposon['sequence']):
                    is_valid = False
                    break
            
            if is_valid:
                filtered.append(transposon)
        
        return filtered

def main():
    # Example usage with the artificial sequence from ex1
    sequence = "AGTCCTTAACTGCCCGGAAGTATTGTACGAACGGACCAACTCAGAGCATTAACCGTAATGCATGTAGGTTTCATACGGTT..."  # Your sequence here
    
    detector = TransposonDetector()
    transposons = detector.detect_transposons(sequence)
    
    print("Detected Transposons:")
    for i, transposon in enumerate(transposons, 1):
        print(f"\nTransposon {i}:")
        print(f"Position: {transposon['start']}-{transposon['end']}")
        print(f"Length: {len(transposon['sequence'])}")
        print(f"Left IR: {transposon['left_ir']}")
        print(f"Right IR: {transposon['right_ir']}")
        print(f"Sequence: {transposon['sequence']}")

if __name__ == "__main__":
    main()