import pytest
from githush.scan import scan_path
from githush.cli import scan
from click.testing import CliRunner


@pytest.fixture
def setup_test_environment(tmp_path):

    test_dir = tmp_path / "test_repo"
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

def test_scan_path_correct_line_numbers(setup_test_environment):
    test_dir = setup_test_environment
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


def test_cli_scan_correct_output(setup_test_environment):
    test_dir = setup_test_environment
    runner = CliRunner()

    result = runner.invoke(scan, [str(test_dir)])

    assert result.exit_code == 0  # Ensure the command runs successfully
    output = result.output

    assert "file_with_secrets.txt" in output
    assert "Line 2: SECRET_KEY=123456789..." in output
    assert "Line 4: password=supersecretpassword123..." in output

    assert "file_without_secrets.txt" not in output