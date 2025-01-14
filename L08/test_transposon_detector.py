from transposon_detector import TransposonDetector

# Your artificial sequence from ex1
sequence = "AGTCCTTAACTGCCCGGAAGTATTGTACGAACGGACCAACTCAGAGCATTAACCGTAATGCATGTAGGTTTCATACGGTT..."

# Create detector and find transposons
detector = TransposonDetector()
transposons = detector.detect_transposons(sequence)

# Print results
print("Detected Transposons:")
for i, transposon in enumerate(transposons, 1):
    print(f"\nTransposon {i}:")
    print(f"Position: {transposon['start']}-{transposon['end']}")
    print(f"Length: {len(transposon['sequence'])}")
    print(f"Left IR: {transposon['left_ir']}")
    print(f"Right IR: {transposon['right_ir']}")