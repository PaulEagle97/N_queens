"""
This script contains several algorithm implementations for solving the N-Queens puzzle.
The puzzle is defined as follows: there is a chess board of size <n>. It is necessary to place
<n> number of queens on it, so that none of the queens attacks any other queen.
The user is given a choice of <n>.

There can be only one queen per row/column/diagonal.
The placement of queens on the board can be represented by a sequence (c0, c1, c2, c3, ... c(n-1)), 
where each element represents a column of the board and its value is the number of a row. Thus, it 
gives us complete coordinates for each queen.
"""
from itertools import permutations


def brute_force(n):
    """
    Brute-force algorithm implementation for the N Queens game solver.
    Input: size of the board (number of cells)
    Output: all permutations-solutions for the given size + counter
    """
    # generate all possible permutations of (0, 1, 2, ... n-1)
    permuts = permutations(range(n), n)
    solutions = set()
    counter = 0

    # iterate through every generated permutation
    for permut in permuts:
        not_valid = False
        # iterate through each element of permutation, except last one
        for idx_1, elem in enumerate(permut[:-1]):
            # iterate through idxs of all next elements
            # up until the end of permutation
            for idx_2 in range(idx_1 + 1, len(permut)):
                counter += 1
                # check if selected cells lie of the same diagonal
                if abs(elem - permut[idx_2]) == idx_2 - idx_1:
                    not_valid = True
                    break
            # break both loops if permutation is not valid
            if not_valid:
                break
        # add to output if is a solution
        if not_valid == False:
            solutions.add(permut)
    
    return solutions, counter


def recursive(prev_moves, board_size):
    """
    A complete recursive function that return a set of all solutions
    for the given size of the board, or empty set otherwise.

    Input: a list of previous moves, a size of the board
    Output: a set with all encountered solutions, or <set()>
    """
    output = set()
    curr_state = list(prev_moves)
    valid_moves = get_valid_moves(curr_state, board_size)

    # BASE CASE
    # check if there are any valid moves
    if len(valid_moves) == 0:
        return output
    # check if it is the last move to be done
    elif len(curr_state) == board_size - 1:
        assert len(valid_moves) == 1, 'There is more than one valid solution for the final row.'
        # add the move to the board and the solution to the set
        curr_state.extend(valid_moves)
        output.add(tuple(curr_state))
        # return the set
        return output

    # iterate through all valid moves
    for move in valid_moves:
        # append each move to the current board state
        next_state = list(curr_state)
        next_state.append(move)
        # call another instance of the function with updated state
        solutions = recursive(next_state, board_size)

        # iterate through a set of all returned solutions
        for solution in solutions:
            # add to the output if solution is not empty set
            if len(solution) > 0:
                output.add(solution)
    
    return output


def recursive_fast(prev_moves, board_size):
    """
    A fast recursive function that returns the first encountered solution
    for the given size of the board, or <None> otherwise.

    Input: a list of previous moves, a size of the board
    Output: a sequence representing a solution, or <None>
    """
    curr_state = list(prev_moves)
    valid_moves = get_valid_moves(curr_state, board_size)

    # BASE CASE
    # check if there are any valid moves
    if len(valid_moves) == 0:
        return None
    # check if it is the last move to be done
    elif len(curr_state) == board_size - 1:
        assert len(valid_moves) == 1, 'There is more than one valid solution for the final row.'
        # add the move to the board and return the solution
        curr_state.extend(valid_moves)
        return tuple(curr_state)
    
    # iterate through all valid moves
    for move in valid_moves:
        # append each move to the current board state
        next_state = list(curr_state)
        next_state.append(move)
        # call another instance of the function with updated state
        solution = recursive_fast(next_state, board_size)
        # return the first solution if found
        if solution != None:
            return solution
        
    # no solutions were found
    return None


def get_valid_moves(prev_moves, board_size):
    """
    Finds all valid next moves, considering the current state of the board.

    Input: a sequence of all previous moves made, a size of the board.
    Output: a set of all valid moves.
    """
    # initialize sets
    valid_moves = set(range(board_size))
    invalid_moves = set()
    # iterate through every previous move
    for idx, move in enumerate(prev_moves):
        # add the move as invalid
        invalid_moves.add(move)
        # calculate the diagonal spread
        diagonal_shift = len(prev_moves) - idx
        # add cells that lie on the diagonal as invalid
        invalid_moves.add(move + diagonal_shift)
        invalid_moves.add(move - diagonal_shift)
    # subsract all invalid moves from all possible moves
    valid_moves.difference_update(invalid_moves)
    
    return valid_moves


def test_get_valid_moves(board_size):
    """
    A testing function for the algorithm of finding all valid next moves.
    """
    failed = set()
    # create a set containing all solutions for the given size
    brute_force_solutions = brute_force(board_size)[0]
    # iterate through each solution and its moves
    for solution in brute_force_solutions:
        print ('<<<--------------->>>')
        print ('Testing the solution:', solution)
        for row, move in enumerate(solution):
            # get a set of all valid moves from the tested function
            valid_moves = get_valid_moves(solution[ : row], board_size)
            print(f'{row + 1}º move:', move)
            print('Valid moves:', valid_moves, '\n')
            # test whether every move of the solution is listed as valid
            if move not in valid_moves:
                failed.add(solution, move)
    
    if len(failed) > 0:
        print ('<<< FAILED >>>:', failed)
    else:
        print ('<<< Test passed! >>>')


def main(user_input):
    
    board_size = int(user_input)
    recurs_sol = recursive_fast([], board_size)
    
    print("Solution:", recurs_sol)


if __name__ == "__main__":
    '''
    Get the size of the chess board and run main() 
    '''
    print('<<< SCRIPT START >>>\n')

    #ask user to choose the dictionary for parsing
    valid_input = False
    while not valid_input:
        user_input = input('Choose the size of the board\n(only natural numbers are allowed)\n')
        valid_input = int(user_input) > 0
    
    main(user_input)
    
    print('\n<<< SCRIPT END >>>\n')    