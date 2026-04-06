# Push: ensure master, bump version, commit, tag, push
push:
    @if [ "$(git rev-parse --abbrev-ref HEAD)" != "master" ]; then \
        echo "Error: not on master branch"; exit 1; \
    fi
    @if [ -n "$(git status --porcelain)" ]; then \
        echo "Error: uncommitted changes"; exit 1; \
    fi
    uv run clasi version bump --no-tag
    git add pyproject.toml
    git commit -m "chore: bump version"
    git tag "v$(uv run clasi version)"
    git push --tags
