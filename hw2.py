import requests
import sys

def getReq(packName, lvl, parentsList):
    if (lvl > 2): return []  #регулирование глубины рекурсии
    packInfo = requests.get(f'https://pypi.org/pypi/{packName}/json').json() #запрашивает информаци о пакете и переводит в формат json
    try:
        reqList = packInfo['info']['requires_dist'] #нахожу список зависимостей
        reqList = set(map(lambda x: x.split()[0], reqList)) #превращаю список в множество что остались уникальные имена
    except:
        return []
    res = []
    for val in reqList:
        pack = val.split()[0]
        if (pack in parentsList): #если пакет есть в паренлисте
            continue
        res.append(f'"{packName}"->"{pack}";') # синтаксис для грфиста
        res.extend(getReq(pack, lvl + 1, parentsList + [packName])) #рекурия дерева
    return res

packages = "TensorFlow, NumPy, SciPy, Pandas, Matplotlib, Keras, SciKit-Learn, PyTorch"
packageList = packages.split(", ")


targetPack = input()
#targetPack = sys.argv[1]
res = getReq(targetPack, 1, [])
res = list(dict.fromkeys(res))
with open("output.txt", 'w') as out:
    out.write("digraph G {\n")
    out.write("\n".join(res))
    out.write("\n}")
