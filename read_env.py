
import os

def read_env():
    try:
        with open('jira-tool-server/.env', 'r') as f:
            content = f.read()
            print("---START---")
            print(content)
            print("---END---")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    read_env()
