import project

board1 = [
    [0, 1, 2],
    [2, 1, 0],
    [0, 1, 0],
]
board2 = [
    [1, 2, 1],
    [2, 1, 2],
    [1, 2, 0],
]

board3 = [
    [0, 1, 0],
    [1, 1, 0],
    [2, 2, 2],
]
board4 = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


def test_get_winner():
    assert project.get_winner(board1) == 1
    assert project.get_winner(board2) == 1
    assert project.get_winner(board3) == 2
    assert not project.get_winner(board4)


def test_get_player():
    assert project.get_player(board1) == 2
    assert project.get_player(board2) == 1
    assert project.get_player(board3) == 1
    assert project.get_player(board4) == 1


def test_ai_move():
    assert project.ai_move(board1) in [(0, 0), (1, 2), (2, 0), (2, 2)]
    assert project.ai_move(board2) in [(2, 2)]
    assert project.ai_move(board3) in [(0, 0), (0, 2), (1, 2)]
    assert project.ai_move(board4) in [(0, 0), (0, 1), (0, 2), (1, 0),
                                       (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
