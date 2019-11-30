"""created by fwk
   2018/06/21
   get code fragment
"""



def getCodeFrag(filepath, start, end):
    result = ""
    with open(filepath, "r") as f:
        result = f.readlines()[start-1:end]
        result = "".join(result)
    return result


if __name__ == "__main__":
    print getCodeFrag("/home/fdse/fwk/SourcererCC/clone-detector/input/dataset/hivedb/src/test/java/org/hivedb/meta/DirectoryTest.java",43,65)


