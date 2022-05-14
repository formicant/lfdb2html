from typing import Iterable, Tuple, Optional, Any
from sqlite3 import connect, Cursor
from data import User, Topic, Message

class LfDb:
    def __init__(self, lfdb_file_name: str):
        # open the db in read-only mode
        self.connection = connect(f'file:{lfdb_file_name}?mode=ro', uri=True)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()
    
    
    def get_user_by_id(self, id: int) -> Optional[User]:
        user = self._get_filtered_users('user.Id = ?', (id,)).fetchone()
        return User(*user) if user is not None else None
    
    def get_user_by_name(self, name: str) -> Optional[User]:
        user = self._get_filtered_users('user.Name = ?', (name,)).fetchone()
        return User(*user) if user is not None else None
    
    def get_topic_by_id(self, id: int) -> Optional[Topic]:
        topic = self._get_filtered_topics('topic.Id = ?', (id,)).fetchone()
        return Topic(*topic) if topic is not None else None
    
    def get_topic_by_name(self, name: str) -> Optional[Topic]:
        topic = self._get_filtered_topics('topic.Name = ?', (name,)).fetchone()
        return Topic(*topic) if topic is not None else None
    
    
    def find_users_by_name(self, name_part: str) -> list[User]:
        users = self._get_filtered_users('user.Name LIKE ?', (f'%{name_part}%',))
        return [User(*row) for row in users]
    
    def find_topics_by_name(self, name_part: str) -> list[Topic]:
        topics = self._get_filtered_topics('topic.Name LIKE ?', (f'%{name_part}%',))
        return [Topic(*row) for row in topics]
    
    def find_messages_by_text(self, text_part: str) -> list[Message]:
        messages = self._get_filtered_messages('message.Text LIKE ?', (f'%{text_part}%',))
        return [Message(*row) for row in messages]
    
    
    def get_user_messages(self, user_id: int) -> Iterable[Message]:
        messages = self._get_filtered_messages('user.Id = ?', (user_id,))
        return (Message(*row) for row in messages)
    
    def get_topic_messages(self, topic_id: int) -> Iterable[Message]:
        messages = self._get_filtered_messages('topic.Id = ?', (topic_id,))
        return (Message(*row) for row in messages)
    
    
    def _get_filtered_users(self, filter: str, filter_params: Tuple) -> Cursor:
        return self.connection.execute(
            f'''SELECT
                    user.Id,
                    user.Name,
                    user.Registered,
                    COUNT(message.Id)
                FROM Users user
                LEFT JOIN Messages message ON message.AuthorId = user.Id
                WHERE {filter}
                GROUP BY user.Id
                ORDER BY user.Id
            ''',
            filter_params
        )
    
    def _get_filtered_topics(self, filter: str, filter_params: Tuple) -> Cursor:
        return self.connection.execute(
            f'''SELECT
                    topic.Id,
                    topic.Name,
                    COUNT(message.Id)
                FROM Topics topic
                LEFT JOIN Messages message ON message.TopicId = topic.Id
                WHERE {filter}
                GROUP BY topic.Id
                ORDER BY topic.Id
            ''',
            filter_params
        )
    
    def _get_filtered_messages(self, filter: str, filter_params: Tuple) -> Cursor:
        return self.connection.execute(
            f'''SELECT
                    message.Id,
                    topic.Id, topic.Name,
                    user.Id, user.Name,
                    message.Time,
                    message.Text
                FROM Messages message
                LEFT JOIN Topics topic ON topic.Id = message.TopicId
                LEFT JOIN Users user ON user.Id = message.AuthorId
                WHERE {filter}
                ORDER BY message.Time
            ''',
            filter_params
        )
