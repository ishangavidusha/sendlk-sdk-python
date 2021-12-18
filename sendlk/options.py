from abc import ABCMeta, abstractmethod
from sendlk.exceptions import SendLKException

class SendLKCodeTemplet(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass
    
    def default(self, code: str) -> str:
        return f"{code} is your verification code."
    
    def validate(self, code: str) -> bool:
        if self.text(code) is None or not isinstance(self.text(code), str):
            return False
        if code not in self.text(code):
            return False
        if self.text(code).count(code) > 1:
            return False
        if len(self.text(code)) > 160:
            return False
        return True
    
    @abstractmethod
    def text(self, code: str) -> str:
        pass

class _DefaultSendLKCodeTemplet(SendLKCodeTemplet):
    def __init__(self) -> None:
        super().__init__()
    
    def text(self, code: str) -> str:
        return self.default(code)

class SendLKVerifyOption:
    def __init__(
        self,
        code_length: int = 4,
        expires_in: int = 3,
        sender_id: str = "",
        code_templet: SendLKCodeTemplet = _DefaultSendLKCodeTemplet(),
        ) -> None:
        
        if not code_length or not isinstance(code_length, int):
            SendLKException(message="Invalid code length.")
        if not expires_in or not isinstance(expires_in, int):
            SendLKException(message="Invalid code expire.")
        if not sender_id or not isinstance(sender_id, str):
            SendLKException(message="Invalid sender id.")
        if not code_templet or not isinstance(code_templet, SendLKCodeTemplet):
            SendLKException(message="Invalid code templet.")
            
        self._code_length = code_length
        self._expires_in = expires_in
        self._sender_id = sender_id
        self._code_templet = code_templet
        
    @property
    def code_length(self) -> int:
        return self._code_length
    
    @property
    def expires_in(self) -> int:
        return self._expires_in
    
    @property
    def sender_id(self) -> str:
        return self._sender_id
    
    def get_text(self, code: str) -> str:
        if self._code_templet.validate(code):
            return self._code_templet.text(code)
        return self._code_templet.default(code)

