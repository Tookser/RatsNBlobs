
LOG_MESSAGE_MAX_LENGTH = 30 #максимальная длина сообщения

#при LOG_DELETE_SIZE этого удаляет уменьшает размер до LOG_MAX_SIZE
LOG_DELETE_SIZE = 100 
LOG_MAX_SIZE = 40


class Log:
    def __init__(self):
        '''_fresh_messages - количество "свежих" сообщений, которые подсвечиваются цветом'''
        self._messages = []
        self._fresh_messages = 0

    @property
    def size(self):
        return len(self._messages)
    
    @property
    def number_of_fresh_messages(self):
        return self._fresh_messages
    
    def return_last_messages(self, n):
        '''возвращает n последних сообщений'''
        if self.size > n:
            return self._messages[-n:]
        else:
            return self._messages[:]
    
    def add_message(self, message):
        '''добавляет сообщение, если их уже было слишком много - удаляет ранние'''
        if len(message) > LOG_MESSAGE_MAX_LENGTH:
            raise Exception("Message too long")
        else:
            self._fresh_messages += 1
            self._messages.append(message)
            if self.size > LOG_DELETE_SIZE:
                self._messages = self._messages[-LOG_MAX_SIZE:]
    
    def refresh(self):
        '''сбрасывает свежие сообщения в старые'''
        self._fresh_messages = 0