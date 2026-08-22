import sys

def main():
    print("Hello World from Python running inside a Docker Container!")
    print(f"Python Version: {sys.version.split()[0]}")

if __name__ == "__main__":
    main()