from uuid import uuid4

def generateTxnId():
    return f'IRMUN{str(uuid4()).replace("-", "")}'

def generateMunarchyId(gender, exp, isSchoolStudent):
    mapGenderToCode = {
        'male': '7',
        'female': '8'
    }
    mapIsSchoolStatusToCode = {
        'UG':'6',
        'PG':'6',
        'others':'6',
        '11th and 12th':'5',
        '10th and below':'4'
    }
    return f"IR25{mapIsSchoolStatusToCode[isSchoolStudent]}{mapGenderToCode[gender]}{str(exp)[0]}{str(uuid4())[0:8].replace('-','')}"