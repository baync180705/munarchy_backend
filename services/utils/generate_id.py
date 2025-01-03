from uuid import uuid4
import os

def generateTxnId():
    return f'IRMUN{str(uuid4()).replace("-", "")}'

def generateMunarchyId(gender, exp, isSchoolStudent):
    file_path = f'{os.path.abspath(os.path.join(os.getcwd(),"current_index.txt"))}'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            index = '00001'
            f.write('1')
    else:
        with open(file_path) as f:
            context = f.read()
        with open(file_path, 'w') as f:
            index = str(int(context)+1).rjust(5,'0')
            f.write(index)
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
    return f"IR25{mapIsSchoolStatusToCode[isSchoolStudent]}{mapGenderToCode[gender]}{str(exp)[0]}{index}"