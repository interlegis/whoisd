# coding: utf-8
def func(x):
    return x+1

def test_answer():
    assert func(3) == 4
def test_wrong_answer():
    assert not func(3) == 5
