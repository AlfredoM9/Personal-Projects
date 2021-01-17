import requests

if __name__ == '__main__':
    while True:
        r = requests.get("http://127.0.0.1:5000/").text
        print(r)