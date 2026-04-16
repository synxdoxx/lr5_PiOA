import Levenshtein
import time

def normalize(text):
    return text.strip().lower()

def find_matches(small_list, big_list, porog=3):
    exact_matches = []
    other_matches = []
    iterations = 0


    normalized_big = [
        {"id": item["id"], "name": normalize(item["name"])}
        for item in big_list
    ]

    big_dict = {normalize(item["name"]): item["id"] for item in big_list}

    for small_item in small_list:
        small_name = normalize(small_item["name"])
        found_exact = False

        if small_name in big_dict:
            exact_matches.append({
                "Название": small_item["name"],
                "ID в базе данных": big_dict[small_name]
            })
            continue

        variants = []

        for big_item in normalized_big:
            if abs(len(small_name) - len(big_item["name"]) <= porog):
                distance = Levenshtein.distance(small_name, big_item["name"])
                iterations += 1

                if distance <= porog:
                    variants.append({
                            "ID в базе данных": big_item["id"],
                            "Название": big_item["name"],
                            "Разница": distance
                        })

        if variants:
                other_matches.append({
                    "Название": small_item["name"],
                    "Возможные варианты": sorted(variants, key=lambda x: x["Разница"])
                })

    return exact_matches, other_matches, iterations

small_list = [ {"id": 1, "name": "iphone 13"}, {"id": 2, "name": "samsng galaxy"}, {"id": 3, "name": "samsung galaxy"}, ]
big_list = [ {"id": 101, "name": "iPhone 13"}, {"id": 102, "name": "Samsung Galaxy"}, {"id": 103, "name": "Xiaomi Redmi"}, {'id': 104, 'name': 'Xiaomi Blue'}, ]

start = time.perf_counter()
exact, other, itr = find_matches(small_list, big_list)
end = time.perf_counter()


print("Точные совпадения:")
print(*exact, sep="\n")

print("Возможные совпадения:")
print(*other, sep="\n")

print(f"Время выполнения: {end - start:.6f} секунд")
print(f'Количество итераций: {itr}')

print(len(small_list), len(big_list))