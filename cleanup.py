import fire
import csv
from postal.parser import parse_address
from postal.expand import expand_address
from postal.normalize import normalize_string
import reaccentue
from collections import defaultdict
import requests


# def read_post_codes():
#     post_codes = defaultdict(list)
#     cities = {}
#     with open("laposte_hexasmal.csv", encoding="utf-8-sig") as csvfile:
#         reader = csv.DictReader(csvfile, delimiter=";")
#         for row in reader:
#             post_codes[row["Code_commune_INSEE"]].append(row["Code_postal"])
#             cities[row["Code_commune_INSEE"]] = row["Nom_commune"]

#     print(f"{len(post_codes)} insee imported")
#     return post_codes, cities


# post_codes, cities = read_post_codes()


# def _find_city(row):
#     zc = post_codes.get(row["insee"])
#     city = cities.get(row["insee"])

#     if not zc or not cities:
#         print("========= c'est la merde !!")
#         return None

#     if len(zc) > 1:
#         print(f"======= plusieurs code postaux pour {row['insee']} :: {zc}")
#         return None, city
#     return zc[0], city


def _get_addok_features(query):
    query = f"https://api-adresse.data.gouv.fr/search/?{query}"
    r = requests.get(query)
    r.raise_for_status

    js = r.json()
    return js.get("features", [])


def _get_addock_label(addr, citycode):
    query = f"q={addr}&citycode={citycode}&limit=1"
    features = _get_addok_features(query)
    if features:
        return features[0]["properties"]["label"]
    # print(f"nothing found for {query}, retrying without the city code constraint")
    features = _get_addok_features(f"q={addr}&limit=1")
    if not features:
        print(f"impossible to find anything for {query}")
        return None

    lbl = features[0]["properties"]["label"]
    print(f"for {addr} ({citycode}) found: {lbl}, check if this is seems ok")

    return lbl


# def cleanup_addr(file_name, output_file):
#     modified_add = []
#     with open(file_name, encoding="utf-8-sig") as csvfile:
#         reader = csv.DictReader(csvfile, delimiter=";")
#         for row in reader:
#             addr = row["adresse"]
#             # print(row)
#             # print(addr)
#             mod_addr = reaccentue.reaccentue(addr)
#             ex = expand_address(addr)
#             print(f"{addr} -- {ex} -> {normalize_string(addr)} || {mod_addr}")
#             # print(f"--->  {r}")

#             normalized = reaccentue.reaccentue(ex[0])

#             parsed_addr = parse_address(addr)
#             typed_addr = {t: v for (v, t) in parsed_addr}
#             if "city" not in typed_addr:
#                 print(f"--- cannot find city for {addr} -- {typed_addr}")
#                 post_code, city = _find_city(row)
#                 if post_code is None:
#                     normalized += reaccentue.reaccentue(f" {city}")
#                 else:
#                     normalized += reaccentue.reaccentue(f" {post_code} {city}")
#             print(f"==> {normalized}")
#             row["adresse"] = normalized
#             modified_add.append(row)

#     with open(output_file, "w", encoding="utf-8-sig") as output:
#         w = csv.DictWriter(output, fieldnames=modified_add[0].keys())
#         w.writeheader()
#         w.writerows(modified_add)

# data = pandas.read_csv(file_name, sep=';', index_col='id', encoding='utf-8')

# data.to_csv("/data/pouet", encoding='utf-8')
# data = pandas.read_csv("/data/pouet", sep=',', index_col='id', encoding='utf-8')
# subprocess.call(["cat", "/data/pouet"])

# print(data)
# print(data['adresse'])


def cleanup_addr(file_name, output_file):
    modified_add = []
    with open(file_name, encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            addr = row["adresse"]
            lbl = _get_addock_label(addr, row["insee"])

            final_addr = addr
            if lbl:
                # row["addok_adresse"] = lbl
                final_addr = lbl

            ex = expand_address(final_addr)[0]
            cased_ex = reaccentue.reaccentue(ex)
            # row["libpostal"] = ex
            # row["libpostal_normalized"] = normalize_string(final_addr)
            # row["final_addr"] = cased_ex
            row["adresse"] = cased_ex

            modified_add.append(row)

    with open(output_file, "w", encoding="utf-8-sig") as output:
        w = csv.DictWriter(output, fieldnames=modified_add[0].keys())
        w.writeheader()
        w.writerows(modified_add)


if __name__ == "__main__":
    fire.Fire()
