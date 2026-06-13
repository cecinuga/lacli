import sys

print(sys.version)              # deve contenere "free-threaded build"
print(sys._is_gil_enabled())

"""
Every line is intended to be an array of the matrix
"""
if __name__ == '__main__':
    file = sys.argv[1]

    matrix = []
    with open(file, 'rb') as f:
        for line in f:
            row = []
            for item in line.strip().split(b','):
                row.append(int(item))
            matrix.append(row)
    print(matrix)
