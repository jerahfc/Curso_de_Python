import copy

PIECES = {
    'wK': '♔', 'wQ': '♕', 'wR': '♖', 'wB': '♗', 'wN': '♘', 'wP': '♙',
    'bK': '♚', 'bQ': '♛', 'bR': '♜', 'bB': '♝', 'bN': '♞', 'bP': '♟',
}

def init_board():
    return [
        ['bR','bN','bB','bQ','bK','bB','bN','bR'],
        ['bP','bP','bP','bP','bP','bP','bP','bP'],
        [None]*8, [None]*8, [None]*8, [None]*8,
        ['wP','wP','wP','wP','wP','wP','wP','wP'],
        ['wR','wN','wB','wQ','wK','wB','wN','wR'],
    ]

def color(p): return p[0] if p else None
def ptype(p): return p[1] if p else None
def opp(c): return 'b' if c == 'w' else 'w'
def in_bounds(r, c): return 0 <= r < 8 and 0 <= c < 8

def print_board(board, flipped=False):
    cols = 'abcdefgh'
    print()
    rows = range(7, -1, -1) if not flipped else range(8)
    col_order = range(8) if not flipped else range(7, -1, -1)
    print('    ' + '  '.join(cols[c] for c in col_order))
    print('   +' + '--+' * 8)
    for r in rows:
        row_num = 8 - r
        row_str = f' {row_num} |'
        for c in col_order:
            p = board[r][c]
            row_str += (PIECES[p] if p else '·') + ' |'
        print(row_str)
        print('   +' + '--+' * 8)
    print('    ' + '  '.join(cols[c] for c in col_order))
    print()

def piece_moves(board, r, c, ep, castle_rights, check_castle=True):
    p = board[r][c]
    if not p: return []
    col, t = color(p), ptype(p)
    moves = []

    def add(nr, nc):
        if in_bounds(nr, nc): moves.append((nr, nc))

    if t == 'P':
        d = -1 if col == 'w' else 1
        start = 6 if col == 'w' else 1
        if in_bounds(r+d, c) and not board[r+d][c]:
            add(r+d, c)
            if r == start and not board[r+2*d][c]:
                add(r+2*d, c)
        for dc in (-1, 1):
            if in_bounds(r+d, c+dc):
                if board[r+d][c+dc] and color(board[r+d][c+dc]) == opp(col):
                    add(r+d, c+dc)
                if ep and (r+d, c+dc) == ep:
                    add(r+d, c+dc)

    elif t == 'N':
        for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
            if in_bounds(r+dr, c+dc) and color(board[r+dr][c+dc]) != col:
                add(r+dr, c+dc)

    elif t == 'K':
        for dr, dc in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            if in_bounds(r+dr, c+dc) and color(board[r+dr][c+dc]) != col:
                add(r+dr, c+dc)
        if check_castle and castle_rights:
            row = 7 if col == 'w' else 0
            cr = castle_rights[col]
            if cr['K'] and not board[row][5] and not board[row][6]:
                if not is_attacked(board,row,4,opp(col)) and not is_attacked(board,row,5,opp(col)) and not is_attacked(board,row,6,opp(col)):
                    add(row, 6)
            if cr['Q'] and not board[row][3] and not board[row][2] and not board[row][1]:
                if not is_attacked(board,row,4,opp(col)) and not is_attacked(board,row,3,opp(col)) and not is_attacked(board,row,2,opp(col)):
                    add(row, 2)

    else:
        if t == 'R':   dirs = [(0,1),(0,-1),(1,0),(-1,0)]
        elif t == 'B': dirs = [(1,1),(1,-1),(-1,1),(-1,-1)]
        else:           dirs = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            while in_bounds(nr, nc):
                if color(board[nr][nc]) == col: break
                add(nr, nc)
                if board[nr][nc]: break
                nr += dr; nc += dc

    return moves

def is_attacked(board, r, c, by_color):
    for rr in range(8):
        for cc in range(8):
            if color(board[rr][cc]) == by_color:
                if (r, c) in piece_moves(board, rr, cc, None, None, False):
                    return True
    return False

def find_king(board, col):
    for r in range(8):
        for c in range(8):
            if board[r][c] == col + 'K':
                return (r, c)
    return None

def apply_move(board, fr, fc, tr, tc, castle_rights, ep, promo=None):
    nb = copy.deepcopy(board)
    new_cr = copy.deepcopy(castle_rights)
    p = nb[fr][fc]
    col, t = color(p), ptype(p)
    new_ep = None

    if t == 'P' and abs(tr - fr) == 2:
        new_ep = ((fr + tr) // 2, fc)
    if t == 'P' and ep and (tr, tc) == ep:
        nb[fr][tc] = None
    if t == 'K':
        new_cr[col]['K'] = False
        new_cr[col]['Q'] = False
        if abs(tc - fc) == 2:
            row = fr
            if tc == 6:
                nb[row][5] = nb[row][7]; nb[row][7] = None
            else:
                nb[row][3] = nb[row][0]; nb[row][0] = None
    if t == 'R':
        if fc == 7: new_cr[col]['K'] = False
        if fc == 0: new_cr[col]['Q'] = False

    nb[tr][tc] = col + promo if promo else p
    nb[fr][fc] = None
    return nb, new_ep, new_cr

def legal_moves_for(board, r, c, ep, castle_rights):
    p = board[r][c]
    if not p: return []
    col = color(p)
    raw = piece_moves(board, r, c, ep, castle_rights, True)
    result = []
    for (tr, tc) in raw:
        nb, _, _ = apply_move(board, r, c, tr, tc, castle_rights, ep)
        kr, kc = find_king(nb, col)
        if not is_attacked(nb, kr, kc, opp(col)):
            result.append((tr, tc))
    return result

def all_legal(board, col, ep, castle_rights):
    moves = []
    for r in range(8):
        for c in range(8):
            if color(board[r][c]) == col:
                for tr, tc in legal_moves_for(board, r, c, ep, castle_rights):
                    moves.append((r, c, tr, tc))
    return moves

def in_check(board, col):
    kr, kc = find_king(board, col)
    return is_attacked(board, kr, kc, opp(col))

def parse_move(s):
    s = s.strip().lower()
    cols = 'abcdefgh'
    if len(s) == 4 and s[0] in cols and s[1].isdigit() and s[2] in cols and s[3].isdigit():
        fc = cols.index(s[0]); fr = 8 - int(s[1])
        tc = cols.index(s[2]); tr = 8 - int(s[3])
        return fr, fc, tr, tc
    return None

def ask_promotion():
    opts = {'q': 'Q', 'r': 'R', 'b': 'B', 'n': 'N'}
    while True:
        choice = input('  Promover peão para (q=Rainha, r=Torre, b=Bispo, n=Cavalo): ').strip().lower()
        if choice in opts:
            return opts[choice]
        print('  Opção inválida.')

def main():
    print('\n♟  XADREZ EM PYTHON  ♔')
    print('Formato de jogada: e2e4, d7d5, etc.')
    print('Comandos: "sair" para encerrar, "virar" para girar o tabuleiro\n')

    board = init_board()
    turn = 'w'
    ep = None
    castle_rights = {'w': {'K': True, 'Q': True}, 'b': {'K': True, 'Q': True}}
    flipped = False
    names = {'w': 'Brancas', 'b': 'Pretas'}

    while True:
        print_board(board, flipped)

        moves = all_legal(board, turn, ep, castle_rights)
        if not moves:
            if in_check(board, turn):
                print(f'  ♛ Xeque-mate! {names[opp(turn)]} vencem!')
            else:
                print('  ½ Empate por afogamento!')
            break

        if in_check(board, turn):
            print(f'  ⚠  Xeque! Turno das {names[turn]}.')
        else:
            print(f'  Turno das {names[turn]}.')

        cmd = input('  Jogada: ').strip().lower()

        if cmd == 'sair':
            print('  Até a próxima!')
            break
        if cmd == 'virar':
            flipped = not flipped
            continue

        parsed = parse_move(cmd)
        if not parsed:
            print('  Formato inválido. Use ex: e2e4\n')
            continue

        fr, fc, tr, tc = parsed
        if color(board[fr][fc]) != turn:
            print('  Essa peça não é sua.\n')
            continue
        if (tr, tc) not in legal_moves_for(board, fr, fc, ep, castle_rights):
            print('  Movimento ilegal.\n')
            continue

        p = board[fr][fc]
        promo = None
        if ptype(p) == 'P' and (tr == 0 or tr == 7):
            promo = ask_promotion()

        board, ep, castle_rights = apply_move(board, fr, fc, tr, tc, castle_rights, ep, promo)
        turn = opp(turn)

if __name__ == '__main__':
    main()