from notifier.base import is_in_archive, Beer


def test_is_in_archive():
    assert is_in_archive(Beer("Three Suns", "Sibeeria"))
    assert is_in_archive(Beer("Three Suns", "Pivovar Sibeeria"))
    assert is_in_archive(Beer("24° Three Suns", "Sibeeria"))
    assert is_in_archive(Beer("Three Suns 24°", "Sibeeria pivovar"))
