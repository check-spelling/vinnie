import os
import pytest

from vinnie.base import Vinnie
from vinnie.exceptions import VinnieConfigError


def test_invalid_options():
    """ Ensure we raise an error if given unknown options """

    # Bad example
    with pytest.raises(VinnieConfigError):
        Vinnie(repo=".", cat_fart=True)

    # Good example
    Vinnie(repo=".", semver=False)


def repo_path(relative):
    """ Build a relative path to our tests/paths/ dir """
    current = os.path.dirname(__file__)
    return os.path.join(current, relative)


def test_validate_repo_path(repo):
    dne = repo_path("paths/does-not-exist")
    not_dir = repo_path("paths/not-a-dir")
    a_dir = repo_path("paths/a-dir")

    # Directory has to exist
    with pytest.raises(VinnieConfigError):
        Vinnie(repo=dne)

    # Has to be a directory
    with pytest.raises(VinnieConfigError):
        Vinnie(repo=not_dir)

    # Has to look like a repo
    with pytest.raises(VinnieConfigError):
        Vinnie(repo=a_dir)

    Vinnie(repo=repo)


def test_url_and_path(repo):
    with pytest.raises(VinnieConfigError):
        Vinnie(repo=repo, repo_url="https://github/")


def test_invalid_url():
    with pytest.raises(VinnieConfigError):
        v = Vinnie(repo_url="g[]")
        v.config.validate_repo_url()

    with pytest.raises(VinnieConfigError):
        v = Vinnie(repo_url="github.com")
        v.config.validate_repo_url()

    v = Vinnie(repo_url="https://github.com/", github_token="XXXX")
    v.config.validate_repo_url()
