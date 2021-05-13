import time
import hashlib
from urllib.request import urlopen, Request

  
# setting the URL monitor changes in home page data
url = Request('https://covid19dashboard.py.gov.in/Home', 
              headers={'User-Agent': 'Mozilla/5.0'})

  
# to perform a GET request and load the 
# content of the website and store it in a var
response = urlopen(url).read()
  
# to create the initial hash
currentHash = hashlib.sha224(response).hexdigest()
print("running")
time.sleep(60) # stops current thread for given time, occurs only at the beginning.
while True:
    try:
        # perform the get request and store it in a var
        response = urlopen(url).read()
          
        # create a hash
        currentHash = hashlib.sha224(response).hexdigest()
          
        # This is used as a cron job to repeat task in specified time. Do every 20 mins!
        time.sleep(1200)
          
        # perform the get request
        response = urlopen(url).read()
          
        # create a new hash
        newHash = hashlib.sha224(response).hexdigest()
  
        # check if new hash is same as the previous hash
        if newHash == currentHash:
            print("no changes in url")
            continue
  
        # if something changed in the hashes
        else:
            # request made to backend api of py care to re fetch data
            urlBackend = Request('pycare-api.herokuapp.com/updateData', 
            headers={'User-Agent': 'Mozilla/5.0'})
  
            # again read the website
            response = urlopen(url).read()
  
            # create a hash
            currentHash = hashlib.sha224(response).hexdigest()
  
            # wait for 30 seconds
            time.sleep(30)
            continue
              
    # To handle exceptions
    except Exception as e:
        print("error")