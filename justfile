# Push: ensure master, bump version, push to remote
push:
    @if [ "$(git rev-parse --abbrev-ref HEAD)" != "master" ]; then \
        echo "Error: not on master branch"; exit 1; \
    fi
    @if [ -n "$(git status --porcelain)" ]; then \
        echo "Error: uncommitted changes"; exit 1; \
    fi
    uv run clasi version bump
    git push
