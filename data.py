from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: int
    name: str
    registered: str
    message_count: int


@dataclass
class Topic:
    id: int
    name: str
    message_count: int


@dataclass
class Message:
    id: int
    topic_id: int
    topic_name: str
    author_id: Optional[int]
    author_name: Optional[str]
    time: str
    text: str
