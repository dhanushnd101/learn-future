def calculate_series():
    # Number of terms
    n = 1_000_000
    
    # We want to calculate: 4 * (1 - 1/3 + 1/5 - 1/7 + ... up to n terms)
    # The i-th term (0-indexed) has a denominator of 2*i + 1
    # and a sign of (-1)^i
    
    total = 0.0
    for i in range(n):
        term = 1.0 / (2 * i + 1)
        if i % 2 == 0:
            total += term
        else:
            total -= term
            
    result = 4 * total
    print(f"Result after {n} terms: {result}")

if __name__ == "__main__":
    calculate_series()
