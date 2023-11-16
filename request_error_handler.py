def request_error_handler(status_code):
 
    if(status_code == 404):
        print(f"Request error: {status_code}")
        print("NOT FOUND: The URI requested is invalid or the resource requested does not exists.")
        
    elif(status_code == 304):
        print(f"Request error: {status_code}")
        print("NOT MODIFIED: There is no new data to return.")
    else:
       print("Generic request error")