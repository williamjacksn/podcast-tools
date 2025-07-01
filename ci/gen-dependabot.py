import gen


def update(ecosystem: str) -> dict:
    return {
        "package-ecosystem": ecosystem,
        "allow": [{"dependency-type": "all"}],
        "directory": "/",
        "schedule": {"interval": "daily"},
    }


ecosystems = ["docker", "github-actions", "uv"]
content = {
    "version": 2,
    "updates": [update(e) for e in ecosystems],
}

gen.gen(content, ".github/dependabot.yaml")
