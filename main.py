import Levenshtein

def normalize(text):
    return text.strip().lower()

def find_matches(small_list, big_list, porog=2):
    full_matches = []
    other_matches = []

    normalized_big = [
        {"id": item["id"], "name": normalize(item["name"])}
        for item in big_list
    ]

    for small_item in small_list:
        small_name = normalize(small_item["name"])
        found_exact = False


        for big_item in normalized_big:
            if small_name == big_item["name"]:
                full_matches.append({
                    "small_id": small_item["id"],
                    "big_id": big_item["id"],
                    "name": small_item["name"]
                })
                found_exact = True
                break

        if not found_exact:
            variants = []

            for big_item in normalized_big:
                distance = Levenshtein.distance(small_name, big_item["name"])

                if distance <= porog:
                    variants.append({
                        "big_id": big_item["id"],
                        "name": big_item["name"],
                        "distance": distance
                    })

            if variants:
                other_matches.append({
                    "name": small_item["name"],
                    "variants": sorted(variants, key=lambda x: x["distance"])
                })

    return full_matches, other_matches

small_list = [
    {"id": 1, "name": "iphone 13"},
    {"id": 2, "name": "samsng galaxy"},
    {"id": 3, "name": "samsung galaxy"},
]

big_list = [
    {"id": 101, "name": "iPhone 13"},
    {"id": 102, "name": "Samsung Galaxy"},
    {"id": 103, "name": "Xiaomi Redmi"},
    {'id': 104, 'name': 'Xiaomi Blue'},
]

full, other = find_matches(small_list, big_list, porog=3)

print("FULL MATCHES:")
for item in full:
    print(item)

print("OTHER MATCHES:")
for item in other:
    print(item)
