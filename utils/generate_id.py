import uuid

def generateTxnId():
    return f'IRMUN{str(uuid.uuid4()).replace("-", "")}'

def generateMunarchyId(name, _id):
    return f"{name[0:4]}{_id}"