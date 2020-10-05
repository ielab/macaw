"""
The message used to represent each interaction in Macaw.

Authors: Hamed Zamani (hazamani@microsoft.com)
"""


class Message:
    def __init__(self, user_interface, user_id, user_info, msg_info, text, timestamp, pdf_url='', web_url=''):
        """
        An object for input and output Message.

        Args:
            user_interface(str): The interface name used for this message (e.g., 'telegram')
            user_id(str or int): The user ID.
            user_info(dict): The dict containing some more information about the user.
            msg_info(dict): The dict containing some more information about the message.
            text(str): The message text.
            timestamp(int): The timestamp of message in milliseconds.
        """
        self.user_id = user_id
        self.user_info = user_info
        self.msg_info = msg_info
        self.text = text
        self.timestamp = timestamp
        self.user_interface = user_interface
        self.pdf_url = pdf_url
        self.web_url = web_url

    @classmethod
    def from_dict(cls, msg_dict):
        """
        Get a Message object from dict.
        Args:
            msg_dict(dict): A dict containing all the information required to construct a Message object.

        Returns:
            A Message object.
        """
        user_interface = msg_dict['user_interface'] if 'user_interface' in msg_dict else None
        user_id = msg_dict['user_id'] if 'user_id' in msg_dict else None
        user_info = msg_dict['user_info'] if 'user_info' in msg_dict else None
        msg_info = msg_dict['msg_info'] if 'msg_info' in msg_dict else None
        text = msg_dict['text'] if 'text' in msg_dict else None
        timestamp = msg_dict['timestamp'] if 'timestamp' in msg_dict else None
        pdf_url = msg_dict['pdf_url'] if 'pdf_url' in msg_dict else ''
        web_url = msg_dict['web_url'] if 'web_url' in msg_dict else ''
        return cls(user_interface, user_id, user_info, msg_info, text, timestamp, pdf_url, web_url)