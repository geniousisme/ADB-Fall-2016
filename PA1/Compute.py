class Compute(object):
    def __init__(self):
        pass

    def multiply(self, vector, multiply_val):
        new_vector = []
        for elem in vector:
            new_vector.append(elem * float(multiply_val))
        return new_vector

    def vector_multiply(self, vector1, vector2):
        return [vector1[i] * vector2[i] for i in xrange(len(vector1))]

    def vector_sum(self, vectors):
        vector_width = len(vectors)
        vector_len = len(vectors[0])
        sum_vector = []
        for j in xrange(vector_len):
            sum_vector.append(sum(vectors[i][j] for i in xrange(vector_width)))
        return sum_vector

