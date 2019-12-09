import hmac
import hashlib
import requests
import urllib3

if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # Removes ssl related warnings. 

    name = 'kalle'
    grade = '5'
    key = 'trivial'
    # api-endpoint 
    URL = "https://eitn41.eit.lth.se:3119/ha4/addgrade.php"

    concat = bytes(name, encoding='utf8') + bytes(grade, encoding='utf8')
    signature = hmac.new(bytes(key, encoding='utf8'), concat, hashlib.sha1).hexdigest()[:20]
    
    elapsed = 0
    
    signature = list(signature)
    finalSig = list(signature)
    for i in range (0,20):
        for char in '1234567890abcdef':
            signature[i] = char
            parameters = {'name':name, 'grade':grade, 'signature':''.join(signature)} 
            total = 0
            for j in range (0, 5):  
                result = requests.get(url = URL, params = parameters, verify=False)
                total += result.elapsed.total_seconds()
            average = total / 5
            print(i, char, average)
            if (average > elapsed):
                finalSig[i] = char
                elapsed = average
                print (elapsed)
                print (finalSig)
        signature[i] = finalSig[i]
        elapsed = 0

    parameters = {'name':name, 'grade':grade, 'signature':signature}        
    result = requests.get(url = URL, params = parameters, verify=False)
    data = result.json() 
    print(data) 
