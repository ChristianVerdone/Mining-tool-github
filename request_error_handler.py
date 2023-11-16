def request_error_handler(status_code):
 
    if(status_code == 404):
        print(f"Request error: {status_code}")
        print("NOT FOUND: The URI requested is invalid or the resource requested does not exists.")
        
    elif(status_code == 304):
        print(f"Request error: {status_code}")
        print("NOT MODIFIED: There is no new data to return.")
        
    elif(status_code == 403):
        print(f"Request error: {status_code}")
        print("403 FORBIDDEN: The request has been refused. See the accompanying message for the specific reason (most likely for exceeding rate limit).")
        
    elif(status_code == 406):
        print(f"Request error: {status_code}")
        print("NOT ACCEPTABLE: The request specified an invalid format.")
    
    elif(status_code == 500):
        print(f"Request error: {status_code}")
        print("INTERNAL SERVER ERROR: Something is horribly wrong.")
        
    elif(status_code == 503):
        print(f"Request error: {status_code}")
        print("SERVICE UNAVAILABLE: The service is up, but overloaded with requests. Try again later.")
    
    elif(status_code == 504): 
        print(f"Request error: {status_code}")
        print("GATEWAY TIMEOUT: Servers are up, but the request couldn’t be serviced due to some failure within our stack. Try again later.")
    
    else:
       print("Generic request error")