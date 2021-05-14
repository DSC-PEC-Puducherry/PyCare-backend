import time
import hashlib
from urllib.request import urlopen, Request
import schedule
  
# setting the URLt to monitor changes in covid data
url = Request('https://covid19dashboard.py.gov.in/BedAvailabilityDetails', 
              headers={'User-Agent': 'Mozilla/5.0'})

url2 = Request('https://covid19dashboard.py.gov.in/Home', 
              headers={'User-Agent': 'Mozilla/5.0'})

  
# to perform a GET request and load the 
# content of the website and store it in a var
response = urlopen(url).read()
response2 = urlopen(url2).read()
  
# to create the initial hash
currentHash = hashlib.sha224(response).hexdigest()
currentHash2 = hashlib.sha224(response2).hexdigest()

print("running")
time.sleep(60) # stops current thread for given time, occurs only at the beginning.

def covidData():
    try:
        # perform the get request and store it in a var
        response = urlopen(url).read()
        response2 = urlopen(url2).read()
          
        # create a hash
        currentHash = hashlib.sha224(response).hexdigest()
        currentHash2 = hashlib.sha224(response2).hexdigest()
          
        # perform the get request
        response = urlopen(url).read()
          
        # create a new hash
        newHash = hashlib.sha224(response).hexdigest()
        newHash2 = hashlib.sha224(response2).hexdigest()
  
        # check if new hash is same as the previous hash
        if newHash == currentHash & newHash2 == currentHash2 :
            print("no changes in url")
  
        # if something changed in the hashes
        else:
            # notify
            urlBackend = Request('pycare-api.herokuapp.com/updateData', 
              headers={'User-Agent': 'Mozilla/5.0'})
  
            # again read the website
            response = urlopen(url).read()
            response2 = urlopen(url2).read()
  
            # create a hash
            currentHash = hashlib.sha224(response).hexdigest()
            currentHash2 = hashlib.sha224(response2).hexdigest()
              
    # To handle exceptions
    except Exception as e:
        print("error")


schedule.every(10).minutes.do(covidData)