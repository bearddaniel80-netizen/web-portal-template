import subprocess
from pathlib import Path


class DockerCompose:
    def __init__(self, compose_file: str):
        self.compose_file = Path(compose_file)

    def up(self) -> None:
        self._run("up", "-d")

    def down(self) -> None:
        self._run("down")

    def ps(self) -> str:
        return self._run("ps", "--status", "running")

    def _run(self, *args: str) -> str:
        command = [
            "docker",
            "compose",
            "-f",
            str(self.compose_file),
            *args,
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())

        return result.stdout