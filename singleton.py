'''Содержит декоратор-синглтон, пока обёрнут только Game и повторный вызов конструктора не используется'''

def singleton(class_):
    '''
    @singleton
    class Classname:
        ...'''
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance