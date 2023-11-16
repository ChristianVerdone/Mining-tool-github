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
   
    else:
       print("Generic request error")