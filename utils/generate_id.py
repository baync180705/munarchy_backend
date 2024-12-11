import uuid

def generateTxnId():
    return f'IRMUN{str(uuid.uuid4()).replace("-", "")}'

def generateMunarchyId(name, number, exp, salt):
    return f"{name[0:4]}{number[0:4]}{salt}{exp}{str(uuid.uuid4())[0:4]}"