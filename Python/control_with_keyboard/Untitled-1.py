# Function to process the list according to the given requirements
def process_list(L):
    # Print the list in reverse order
    reverse_list = L[::-1]
    print(*reverse_list)

    # Print every 3rd number with 3 added to it
    third_with_3_added = [L[i] + 3 for i in range(3, len(L), 3)]
    print(*third_with_3_added)

    # Print every 5th number with 7 subtracted from it
    fifth_with_7_subtracted = [L[i] - 7 for i in range(5, len(L), 5)]
    print(*fifth_with_7_subtracted)

    # Sum of all numbers with an index between 3 and 7 (inclusive)
    sum_between_3_and_7 = sum(L[2:7])  # Use indices 2 to 6 to include elements at positions 3 to 7.
    print(sum_between_3_and_7)

# Input the number of test cases
T = int(input())

# Iterate through each test case
for _ in range(T):
    n = int(input())  # Input the length of the list
    L = list(map(int, input().split()))  # Input the list of numbers
    process_list(L)  # Process and print the list according to the requirements
