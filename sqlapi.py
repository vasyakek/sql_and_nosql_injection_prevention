from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/sqldetection")
def sqldetect(input: Union[str,None] = None ):
        if input == None:
                info = 'no given arguments or array is given'
                is_secure = False
                return { "is_secure": is_secure, "value":input,"info":info}
        info = 'safe request'
        input =  str(input)
        is_secure = True
        if any(k in ('"', "'", "(", ")", "{", "}", "[", "]",";",":") for k in input):
                is_secure = False
                info = 'request contains illegal characters'
        return { "is_secure": is_secure, "value":input,"info":info}