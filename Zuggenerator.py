_M_HV = [(0, -1), (0, 1), (-1, 0), (1, 0)]
_M_DI = [(-1, -1), (1, -1), (-1, 1), (1, 1)]

_MOVES = {'r': [7, *_M_HV],
          'b': [7, *_M_DI],
          'k': [1, *_M_HV, *_M_DI],
          'q': [7, *_M_HV, *_M_DI],
          'n': [1, (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (-1, 2), (1, 2)],

          'p': [2, (0, 1)],
          'P': [2, (0, -1)],
          'pc': [1, (-1, 1), (1, 1)],
          'Pc': [1, (-1, -1), (1, -1)]}

_GRUNDLINIE = [1, 6]

BRETT = {(s, z): s % 2 == z % 2 for s in range(8) for z in range(8)}


def ZugGenerator(weiss, position):
    züge = []
    pseudo, königspos = _pseudoZugGenerator(weiss, position)
    for zug in pseudo:
        zug_ausführen(zug, position, königspos)
        if not ImSchach(weiss, position, königspos[weiss]):
            züge.append(zug)
        zug_zurücknehmen(zug, position, königspos)

    return züge

def ImSchach(weiss, position, von):
    for figs, moves in _MOVES.items():#
        if figs in 'pP': continue
        for ds, dz in moves[1:]:
            for m in range(1, moves[0] + 1):
                zu = von[0] + ds * m, von[1] + dz * m
                if zu not in BRETT: break
                if zu in position:
                    if position[zu].isupper() == weiss:
                        break
                    else:
                        if position[zu].lower() in figs:
                            return True
                        break

def zug_ausführen(zug, position, königspos):
    fig, von, zu, capture, umwandlung = zug
    position[zu] = position.pop(von)

    if umwandlung:
        position[zu] = 'Q' if fig.isupper() else 'q'
    if fig in 'kK':
        königspos[fig.isupper()] = zu

def zug_zurücknehmen(zug, position, königspos):
    fig, von, zu, capture, umwandlung = zug
    position[von] = position.pop(zu )

    if capture:
        position[zu] = capture
    if umwandlung:
        position[von] = 'P' if fig.isupper() else 'p'
    if fig in 'kK':
        königspos[fig.isupper()] = von

def _pseudoZugGenerator(weiss, position):
    pseudo, königspos = [], [0, 0]
    for von, fig in position.items():
        if fig.isupper() != weiss: continue
        if fig in 'pP':
            _ZügeBauern(weiss, fig, von, position, pseudo)
        f = fig.lower()
        if f == 'k': königspos[weiss]
        richtungen = _MOVES[f][1:]
        multiplikator = _MOVES[f][0]
        for ds, dz in richtungen:
            for m in range(1, multiplikator + 1):
                zu = von[0] + ds * m, von[1] + dz * m
                if zu not in BRETT: break
                if zu in position and position[zu].isupper() == weiss: break
                if zu in position and position[zu].isupper() != weiss:
                    pseudo.append((fig, von, zu, position[zu], False))
                    break
                else:
                    pseudo.append((fig, von, zu, False, False))
    return pseudo, königspos


def _ZügeBauern(weiss, fig, von, position, pseudo):
    #  Stiller Zug
    for ds, dz in _MOVES[fig][1:]:
        for m in range(1, _MOVES[fig][0] + 1):
            zu = von[0], von[1] + dz * m
            if zu not in BRETT or zu in position: break
            if m == 2 and von[1] != _GRUNDLINIE[weiss]: break
            if zu[1] in (0, 7):
                pseudo.append((fig, von, zu, False, True))
            else:
                pseudo.append((fig, von, zu, False, False))
    #  SchlagZug
    for ds, dz in _MOVES[fig+'c'][1:]:
        zu = von[0] + ds, von[1] + dz
        if zu not in position: continue
        if position[zu].isupper() == weiss: continue
        if zu[1] in (0, 7):
            pseudo.append((fig, von, zu, position[zu], True))
        else:
            pseudo.append((fig, von, zu, position[zu], False))
