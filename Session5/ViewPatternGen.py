import json
import multiprocessing as mp
import os


def readDataFromJsonFile(fileName):
    f = open(fileName, 'r')
    data = json.load(f)
    lst, op = [], []
    lst.append(os.path.split(fileName)[1][:-14])
    lst.append(list(data['Unique_Column'].keys()))
    b = False
    for k, v in data.items():
        if b:
            for k1, v1 in list(map(list, v.items())):
                tp = lst.copy() + [k, k1]
                if k1 in data['Check_attributes'].keys():
                    tp += [v1 + '/@' + data['Check_attributes'][k1]]
                else:
                    tp += [v1]
                if k1 in data['Check_instance']:
                    tp += [data['Check_instance'][k1]]
                else:
                    tp += ['Last']
                op.append(tp)
        b = b or k == 'Grouping_Column'
    return op


if __name__ == "__main__":
    pool = mp.Pool(processes=mp.cpu_count())
    path_to_json = os.path.dirname(os.path.realpath(__file__))
    json_files = [path_to_json + '\\' + pos_json for pos_json in os.listdir(path_to_json)
                  if pos_json.endswith('_patterns.json')]
    resultList = sum(pool.map(readDataFromJsonFile, json_files), [])
    pool.close()
    pool.join()
    print(resultList)
