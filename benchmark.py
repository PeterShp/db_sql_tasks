import requests
import time

API_URL = "http://localhost:5000"

def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        return elapsed, result
    return wrapper

@measure_time
def insert_data(n, token):
    for i in range(n):
        data = {
            "title": f"Book {i}",
            "author_name": "Author Test",
            "genre_name": "Genre Test"
        }
        requests.post(f"{API_URL}/books", json=data, headers={"Authorization": f"Bearer {token}"})
    return n

@measure_time
def select_all(token):
    r = requests.get(f"{API_URL}/books", headers={"Authorization": f"Bearer {token}"})
    return r.json()

@measure_time
def select_one(record_id, token):
    r = requests.get(f"{API_URL}/books/{record_id}", headers={"Authorization": f"Bearer {token}"})
    return r.status_code

@measure_time
def update_one(record_id, new_title, token):
    data = {"title": new_title}
    r = requests.put(f"{API_URL}/books/{record_id}", json=data, headers={"Authorization": f"Bearer {token}"})
    return r.status_code

@measure_time
def delete_one(record_id, token):
    r = requests.delete(f"{API_URL}/books/{record_id}", headers={"Authorization": f"Bearer {token}"})
    return r.status_code

def login():
    data = {"username": "admin", "password": "admin"}
    r = requests.post(f"{API_URL}/login", json=data)
    if r.status_code == 200:
        return r.json()['access_token']
    else:
        raise Exception("Login failed")

def run_benchmarks():
    test_sizes =  [1000] 
    #test_sizes = [10000, 100000,  1000000] занадто багато, оскільки довго чекати результат, тому в прикріпленні до завдання тільки на 1000

    results = []

    for size in test_sizes:
        requests.delete(f"{API_URL}/reset")

        token = login()

        insert_time, _ = insert_data(size, token)
        select_all_time, all_books = select_all(token)
        select_one_time, _ = select_one(1, token)
        update_one_time, _ = update_one(1, "Updated Title", token)
        delete_one_time, _ = delete_one(1, token)

        results.append({
            "size": size,
            "insert_time": insert_time,
            "select_all_time": select_all_time,
            "select_one_time": select_one_time,
            "update_one_time": update_one_time,
            "delete_one_time": delete_one_time
        })

    return results

if __name__ == "__main__":
    benchmark_results = run_benchmarks()
    print("Size | Insert_time(s) | Select_all_time(s) | Select_one_time(s) | Update_one_time(s) | Delete_one_time(s)")
    for r in benchmark_results:
        print(f"{r['size']} | {r['insert_time']:.4f} | {r['select_all_time']:.4f} | {r['select_one_time']:.4f} | {r['update_one_time']:.4f} | {r['delete_one_time']:.4f}")
