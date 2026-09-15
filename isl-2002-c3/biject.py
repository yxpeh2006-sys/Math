def permutations(n):
    '''
    Outputs a list of tuples representing permutations of (1, 2, ..., n)
    '''
    permutations = []                                   # list of permutations in working progress
    current_candidates = set(i for i in range(1, n+1))  # elements not present in permutation yet
    current = []                                        # permutation in working progress

    def backtrack(current, current_candidates):
        if not current_candidates:                  # if nothing left unused
            permutations.append(tuple(current))     # current permutation is complete
            return
        for i in current_candidates.copy():         # for each unused element
            current.append(i)                       # add it to current permutation
            current_candidates.remove(i)            # remove unused element from set of unused elements
            backtrack(current, current_candidates)  # backtrack
            current.remove(i)                       # reset: remove element from current permutation
            current_candidates.add(i)               # reset: add back element to set of unused elements

    backtrack(current, current_candidates)      # run the backtracking algorithm
    return permutations

def permutation_to_full(permutation):
    '''
    Returns the full sequence that the given permutation bijects to as a tuple
    '''
    n = len(permutation)            # store length of permutation
    full = [0 for _ in range(n)]    # initiates full sequence to all 0s
    current = 1     # current element of permutation that we are searching for
    passing = 1     # the number of passes across the permutation we are at now

    while current <= n:     # while we are still searching for an element of the permutation
        for i in range(n):  # pass through the permutation backwards
            if permutation[n - 1 - i] == current:   # if we find the required element
                full[n - 1 - i] = passing           # update the full sequence there
                current += 1                        # search for the next element
        passing += 1        # keep track of the number of passes we have made
    
    return tuple(full)
        
def full_to_permutation(full):
    '''
    Returns the permutation that the given full sequence bijects to as a tuple
    '''
    n = len(full)                           # store length of full sequence
    permutation = [0 for _ in range(n)]     # initialises the permutation as all 0s
    current = 1     # element to be added to the permutation when we find the full sequence element
    passing = 1     # current element of the full sequence that we are searching for

    while current <= n:     # while not all elements have been added to the permutation
        for i in range(n):  # pass through the full sequence backwards
            if full[n - 1 - i] == passing:          # if we find the full sequence element
                permutation[n - 1 - i] = current    # update the permutation there
                current += 1                        # update the next addition
        passing += 1        # keep track of the number of passes we have made
    return tuple(permutation)

def map_permutations(permutations):
    '''
    Returns a dictionary of permutation : full sequence
    '''
    return {tuple(permutation): permutation_to_full(permutation) for permutation in permutations}

def map_fulls(fulls):
    '''
    Returns a dictionary of full sequence : permutation
    '''
    return {tuple(full): full_to_permutation(full) for full in fulls}

def print_map_permutations(permutations):
    '''
    Prints the dictionary of permutation : full sequence
    '''
    for key, value in map_permutations(permutations).items():
        print(f'{key}: {value}')

def print_map_fulls(fulls):
    '''
    Prints the dictionary of full sequence : permutation
    '''
    for key, value in map_fulls(fulls).items():
        print(f'{key}: {value}')

def main():
    while True:
        input_char = input('Choose one:\nGenerate all (A)\nMap a permutation to a full sequence (P)\nMap a full sequence to a permutation (F)\n')

        try:
            char = str(input_char)
        except Exception():
            raise Exception('Please type one of A, P, or F.')

        if char == 'A':
            input_n = input('Select n: ')

            try:
                n = int(input_n)
            except Exception():
                raise Exception('Please input a positive integer.')
            if n <= 0:
                raise Exception('Please input a positive integer.')

            print_map_permutations(permutations(n))
            break

        elif char == 'P':
            input_perm = input('Type a permutation with space-separated elements.\n')

            try:
                perm = [int(number) for number in input_perm.split()]
            except Exception():
                raise Exception('Please input space-separated positive integers.')

            n = len(perm)
            appears = [False for _ in range(n)]   # keeps track of what numbers have appeared
            for k in perm:
                if k <= 0:
                    raise Exception('Permutation can only contain positive integers.')
                elif k > n:
                    raise Exception('Permutation does not contain all consecutive integers from 1 to its length.')

                if appears[k - 1]:
                    raise Exception('Permutation contains duplicates.')
                else:
                    check[k - 1] = True

            print(permutation_to_full(perm))
            break

        elif char == 'F':
            input_full = input('Type a full sequence with space-separated elements.\n')

            try:
                full = [int(number) for number in input_full.split()]
            except Exception():
                raise Exception('Please input space-separated positive integers.')

            n = len(full)
            appeared = set()    # keep track of what numbers have appeared
            check = {1: False}  # keep track of what values' validities still has to be checked

            for k in full:
                appeared.add(k)
                if k > 1:
                    if k not in check:              # first occurrence of k
                        if (k - 1) in appeared:     # if (k-1) has not appeared, k is not yet valid
                            check[k] = False
                        else:                       # if (k-1) has appeared, k is definitely valid
                            check[k] = True
                    else:                                       # not the first occurrence of k
                        if check[k] and (k - 1) in appeared:    # if (k-1) has appeared, k is definitely valid
                            check[k] = False

            if any(check.values()):     # if any number's validity still has not been confirmed
                raise Exception('Input sequence does not satisfy the conditions of a full sequence.')

            print(full_to_permutation(full))
            break

if __name__ == '__main__':
    main()
