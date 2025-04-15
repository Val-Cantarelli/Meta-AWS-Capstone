# scripts/cli.py

import argparse
import time
from jwt_client import JWTClient

def main():
    parser = argparse.ArgumentParser(description="CLI to test JWT auth")

    parser.add_argument("--env", choices=["local", "prod"], default="local", help="Ambiente da API")
    parser.add_argument("--username", required=True, help="User")
    parser.add_argument("--password", required=True, help="Password")
    parser.add_argument("--loop", type=int, default=1, help="How many times repeat the requisition")
    parser.add_argument("--interval", type=int, default=30, help="Gap between requisitions(seconds)")
    parser.add_argument("--endpoint", default="/api/menu-items/", help="Endpoint")

    args = parser.parse_args()

    client = JWTClient(args.env, args.username, args.password)

    if not client.load_tokens():
        if not client.login():
            print("Login failed.")
            return

    for i in range(args.loop):
        print(f"\n Trail {i+1}/{args.loop}")
        response = client.request_with_refresh(args.endpoint)
        if response:
            print(f" Status: {response.status_code}")
            try:
                print(response.json())
            except:
                print("Answer is not a JSON.")
        else:
            print("Error at requisition.")
        if i < args.loop - 1:
            time.sleep(args.interval)

if __name__ == "__main__":
    main()
