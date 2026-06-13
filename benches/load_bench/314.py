import sys

"""
Every line is intended to be an array of the matrix
"""
if __name__ == '__main__':
    file = sys.argv[1]

    matrix = []
    with open(file, 'r') as f:
        for line in f:
            row = []
            for item in line.strip().split(','):
                row.append(int(item))
            matrix.append(row)
    print(matrix)
