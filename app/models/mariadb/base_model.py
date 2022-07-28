class BaseModel:
    def to_dict(self):
        dic = {}
        for k,v in self.__dict__.items():
            if k.startswith('_') or k.startswith('__'):
                pass
            else:
                dic[k] = v
        
        return dic
