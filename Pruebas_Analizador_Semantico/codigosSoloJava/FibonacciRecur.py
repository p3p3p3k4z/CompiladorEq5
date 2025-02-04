def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 2) + fibonacci(n - 1)

if __name__ == "__main__":
    print("Print Fibonacci Series Using Recursion in Python")

    MAX = 10
    for i in range(MAX):
        print(fibonacci(i), end=" ")
