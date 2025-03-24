import os
import subprocess

import pygit2
import pytest
import tempfile
from githush.scan import scan_path
from githush.cli import scan
from click.testing import CliRunner


@pytest.fixture
def setup_test_environment_folder(tmp_path):

    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()

    # File with secrets
    file_with_secrets = test_dir / "file_with_secrets.txt"
    file_with_secrets.write_text(
        "This is a clean line.\n"
        "This line contains a SECRET_KEY=123456789.\n"
        "Another clean line here.\n"
        "This line has a password=supersecretpassword123.\n"
    )

    clean_file = test_dir / "file_without_secrets.txt"
    clean_file.write_text("This is a completely clean file.\nNo secrets here.\n")

    return test_dir

@pytest.fixture
def setup_test_environment_repo():
    
    dir_path = tempfile.mkdtemp()
    test_repo = pygit2.init_repository(dir_path, False)

    secret_file = os.path.join(dir_path, "secrets.txt")
    with open(secret_file, "w") as f:
        f.write("password: hunter2")
    
    test_repo.index.add(os.path.relpath(secret_file, dir_path)) 
    test_repo.index.write()

    return dir_path

def test_scan_path_correct_line_numbers(setup_test_environment_folder):
    test_dir = setup_test_environment_folder
    results = scan_path(str(test_dir))
    expected_results = [
        (
            str(test_dir / "file_with_secrets.txt"),
            [
                (2, "SECRET_KEY=123456789"),
                (4, "password=supersecretpassword123."), #included the trailing dot because it's a valid character for passwords
            ],
        )
    ]

    assert len(results) == 1  # One file should have secrets
    assert results == expected_results


def test_cli_scan_correct_output(setup_test_environment_folder):
    test_dir = setup_test_environment_folder
    runner = CliRunner()

    result = runner.invoke(scan, [str(test_dir)])

    assert result.exit_code == 1
    output = result.output

    assert "file_with_secrets.txt" in output
    assert "Line 2: SECRET_KEY=123456789" in output
    assert "Line 4: password=supersecretpassword123" in output

    assert "file_without_secrets.txt" not in output


def test_scan_repo(setup_test_environment_repo):
    test_dir = setup_test_environment_repo

    results = scan_path(str(test_dir), True)
    expected_results = [
        (
            str("secrets.txt"),
            [
                (1, "password: hunter2")
            ],
        )
    ]
    assert len(results) == 1  # One file should have secrets
    assert results == expected_results