import fire
import csv
import requests
import re


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


replace_av_regex = re.compile(r"\b[Aa]v\b")


def _manual_cleanup(addr):
    return replace_av_regex.sub("Avenue", addr)


def cleanup_addr(file_name, output_file):
    modified_add = []
    with open(file_name, encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            addr = row["adresse"]
            lbl = _get_addock_label(addr, row["insee"])

            if lbl:
                lbl = _manual_cleanup(lbl)
                row["adresse"] = lbl

            modified_add.append(row)

    with open(output_file, "w", encoding="utf-8-sig") as output:
        w = csv.DictWriter(output, fieldnames=modified_add[0].keys())
        w.writeheader()
        w.writerows(modified_add)


if __name__ == "__main__":
    fire.Fire()
