class BaseModel:
    def to_dict(self):
        print(f'######### TO_DICT')
        dic = {}
        for k,v in self.__dict__.items():
            if k.startswith('_') or k.startswith('__'):
                pass
            else:
                dic[k] = v
        
        return dic
