def cross(A, B):
    return [a + b for a in A for b in B]

digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits

squares = cross(rows, cols)

# creating unit list
unitlist = ( [cross(rows, c) for c in cols] + [cross(r, cols) for r in rows] + [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')] )

# defining units for each square.
# each square will be in 3 units and these units will be represented by the key defined as square itself
units = dict((s, [u for u in unitlist if s in u]) for s in squares)

# creating peers for each square
peers = dict(( s, set(sum(units[s], [])) - set([s])) for s in squares)


# testing
def test():
    "A set of unit tests."
    assert len(squares) == 81
    assert len(unitlist) == 27
    assert all(len(units[s]) == 3 for s in squares)
    assert all(len(peers[s]) == 20 for s in squares)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2','G2', 'H2', 'I2'], ['C1' ,'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers['C2'] == set(['A1', 'A2', 'A3', 'A3', 'B1', 'B2', 'B3', 'C1', 'C3', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'])

    print('All tests pass.')

test()

""" Converting grid to a dictionary of the possible values each square can take [square : values]."""
def parse_grid ( grid ):
    # For start define grid in which square can have any value and then assign values for the original grid
    values = dict((s,digits) for s in squares)
    for s,d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False ## Fail if d from grid can not be assigned to square
    return values

def grid_values( grid ):
    # converting grid into a dictionary of [squares : char] with '0' or '.' for empties
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))

def assign( values, s, d):
    """ Eliminate all other values from s except d from values[s]
        Return values , except return False if a contradiction is detected. """
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d1) for d1 in other_values):
        return values
    else:
        return False

def eliminate(values, s, d):
    if d not in values[s]:    # d has been already deleted from values[s]
        return values
    values[s] = values[s].replace(d, '')
    ## 1. if d is the only value in values[s] delete d from peers[s]
    if len(values[s]) == 0:
        return False   # last value from values[s] has been deleted
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s1, d2) for s1 in peers[s]):
            return False
    ## 2. if there is only one square in which d can be put in a unit
    for u in units[s]:
        dplace = [s2 for s2 in u if d in values[s2]]
        if len(dplace) == 0 :
            return False
        elif len(dplace) == 1:
            if not assign(values, dplace[0], d):
                return False
        
    return values

def display(values):
    width = 1+max(len(values[s]) for s in squares)
    line = '+'.join(['-' * (width*3)] * 3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '') for c in cols))
        if r in 'CF' : print(line)
    print


grid = '506031070437005000010467008029178300000000026300050000805004910003509087790086004'
#grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
#grid = '000000500302070910600900000000000026020300159790605080109700000450000230038450600'
#grid = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'

#display(solve(grid))

def solve(grid): return search(parse_grid(grid))

def search(values):
	"Using depth-first search and propogation, try all possible values."
	if values is False:
		return False ## Failed earlier
	if all(len(values[s]) == 1 for s in squares):
		return values ## Solved !
	## Choose the unfilled squres s with the fewest possibilities
	n,s = min(( len( values[s] ), s) for s in squares if len(values[s]) > 1 )
	return some(search(assign(values.copy(), s, d)) for d in values[s] )

def some(seq):
	"Return some element of seq that is true"
	for e in seq:
		if e: return e
	return False

display(solve(grid))
