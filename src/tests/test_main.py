from ultimate_fastapi_tutorial import __version__


def test_main() -> None:
    assert isinstance(__version__, str)
