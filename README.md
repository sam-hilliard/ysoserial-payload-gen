# Ysoserial Payload Generator
Wrapper around ysoserial-jar that creates a list of base64-encoded payloads for ease of testing
Creates the perfect environment for [ysoserial](github.com/frohoff/ysoserial)

# Running

1. Build the container
``` shell
$ docker build -t ysoserial-env .
```

2. Run the container
``` shell
$ docker run --rm \
    -v "$PWD:/app" \
    ysoserial-env
```

Optionally, use the `run.sh` script to automate these steps.

# Detection mode

- use `-d` to create a list of base64-encoded payloads to see which library is vulnerable:

``` shell
$ ./run.sh -d <example.oastify.com>
```
- use the generated payloads to fuzz and get pingbacks to identify which library is vuln.

