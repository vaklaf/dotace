
class CustomMessage:
    
    def __init__(self,data:dict):
        self.module:str = data['module']
        self.message:str = data['message']
        self.data:dict = data['data']
    
    def __str__(self)->str:
        return f'{self.module}: {self.message} -data: {self.data}'