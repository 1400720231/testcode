def file_to_json(file_path=""):
    if not file_path:
        return
    result_list = list()
    with open(file_path, encoding="utf-8") as f:
        for line in f.readlines()[1:]:
            print(line.strip("\n").strip("\r").strip("\t"))
            # [{"id": "0", "cpu": "Intel 8v Core", "memory": "8Gi", "disk": "500Gb"}]
            result_list.append({
                "id": line.split(",")[0],
                "cpu": line.split(",")[1],
                "memory": line.split(",")[2],
                "disk": line.split(",")[3],
            })

    print(result_list)


if __name__ == "__main__":
    file_to_json(file_path="/Users/xiongyao/project/test/test-code-env/testcode/plans/plan_15.json")
