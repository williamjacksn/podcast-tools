import json
import pathlib


def gen(content: dict, target: str) -> None:
    pathlib.Path(target).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(target).write_text(
        json.dumps(content, indent=2, sort_keys=True), newline="\n"
    )


def gen_dependabot() -> None:
    target = ".github/dependabot.yaml"
    content = {
        "version": 2,
        "updates": [
            {
                "package-ecosystem": e,
                "allow": [{"dependency-type": "all"}],
                "directory": "/",
                "schedule": {"interval": "weekly"},
            }
            for e in ["docker", "github-actions", "uv"]
        ],
    }
    gen(content, target)


def main() -> None:
    gen_dependabot()


if __name__ == "__main__":
    main()
