from src.utils import create_url


def test_create_url_includes_host_user_password_and_action():
    url = create_url(
        "https://server.fseconomy.net/fsagentFSX?",
        "test-user",
        "test-password",
        "accountCheck",
    )

    assert url == (
        "https://server.fseconomy.net/fsagentFSX?"
        "user=test-user&pass=test-password&action=accountCheck"
    )
