import threading, requests, asyncio


def a():
    while True:
        response = requests.get("https://xn--80aapkb3algkc.xn--j1afpl.xn--p1ai/")
        print(f"{response.status_code}")
async def main
if __name__ == "__main__":
    threads = []
    for i in range(20):
        threads.append(threading.Thread(target=a))

    for thread in threads:
        thread.start()