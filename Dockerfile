# syntax=docker/dockerfile:1

# It's important that this is Debian 12 to match the distroless image.
FROM debian:12-slim AS build

RUN --mount=type=cache,target=/var/lib/apt/lists \
    --mount=type=cache,target=/var/cache/apt \
    rm -f /etc/apt/apt.conf.d/docker-clean \
    && apt-get update \
    && apt-get install --no-install-recommends --yes python3-venv git

# Don't write .pyc bytecode files. These speed up imports when the program is
# loaded. There's no point doing that in a container where they'll never be
# persisted across restarts.
ENV PYTHONDONTWRITEBYTECODE=true

# Use Hatch to build a wheel. The build stage must do this in a venv because
# Debian doesn't have a hatch package, and it won't let you install one globally
# using pip.
WORKDIR /build
RUN --mount=target=. \
    --mount=type=cache,target=/root/.cache/pip \
    python3 -m venv /venv/build \
    && /venv/build/bin/pip install hatch \
    && /venv/build/bin/hatch build -t wheel /whl

# Create a fresh venv and install only the function wheel into it.
RUN --mount=type=cache,target=/root/.cache/pip \
    python3 -m venv /venv/fn \
    && /venv/fn/bin/pip install /whl/*.whl

# Copy the function venv to our runtime stage. It's important that the path be
# the same as in the build stage, to avoid shebang paths and symlinks breaking. 
FROM gcr.io/distroless/python3-debian12 AS image
WORKDIR /
COPY --from=build /venv/fn /venv/fn
EXPOSE 9443
USER nonroot:nonroot
ENTRYPOINT ["/venv/fn/bin/function"]
