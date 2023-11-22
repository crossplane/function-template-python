# function-template-python
[![CI](https://github.com/crossplane/function-template-python/actions/workflows/ci.yml/badge.svg)](https://github.com/crossplane/function-template-go/actions/workflows/ci.yml)

A template for writing a [composition function][functions] in [Python][python].

To learn how to use this template:

* [Learn about how composition functions work][functions]

If you just want to jump in and get started:

1. Replace `function-template-python` with your function's name in
   `pyproject.toml` and `package/crossplane.yaml`.
1. Add your logic to `RunFunction` in `function/fn.py`
1. Add tests for your logic in `test/test_fn.py`
1. Update this file, `README.md`, to be about your function!

This template uses [Python][python], [Docker][docker], and the [Crossplane
CLI][cli] to build functions.

```shell
# Lint the code - see pyproject.toml
hatch run lint:check

# Run unit tests - see tests/test_fn.py
hatch run test:unit

# Build the function's runtime image - see Dockerfile
$ docker build . --tag=runtime

# Build a function package - see package/crossplane.yaml
$ crossplane xpkg build -f package --embed-runtime-image=runtime
```

[functions]: https://docs.crossplane.io/latest/concepts/composition-functions
[python]: https://python.org
[docker]: https://www.docker.com
[cli]: https://docs.crossplane.io/latest/cli