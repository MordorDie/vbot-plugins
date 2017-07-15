import os


def create_list(path):
    list = []

    for v in os.listdir(path):
        if v == "__dir__":
            continue

        if os.path.isdir(v):
            list.append(f"dir;{v}")
            create_list((path + "/" if path else "") + v + "/")

        elif path:
            list.append(f"file;{v}")

    with open(f"{path if path else ''}dir", "w") as f:
        f.write("\n".join(list))


if __name__ == "__main__":
    create_list(None)
