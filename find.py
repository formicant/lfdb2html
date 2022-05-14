from argparse import ArgumentParser
from lfdb import LfDb

default_db_file = 'lfdb_2021-11-16.sqlite'

parser = ArgumentParser(description='Finds users, topics, or messages by a substring.')

what_to_find = parser.add_mutually_exclusive_group(required=True)
what_to_find.add_argument('-u', '--user', action='store_true', help='Find users')
what_to_find.add_argument('-t', '--topic', action='store_true', help='Find topics')
what_to_find.add_argument('-m', '--message', action='store_true', help='Find messages')

parser.add_argument('-d', '--database', help=f'Sqlite database file. ("{default_db_file}" is used by default)')
parser.add_argument('substring', help='A substring to find')

args = parser.parse_args()

db_file = args.database or default_db_file


with LfDb(db_file) as lfdb:
    
    if args.user:
        users = lfdb.find_users_by_name(args.substring)
        count = len(users)
        
        print(f'Users found: {count}')
        if count > 0:
            print('   Id  Registered  Posts  Name')
        for user in users:
            print(f'{user.id:5d}  {user.registered[:10]}  {user.message_count:5d}  {user.name}')
    
    if args.topic:
        topics = lfdb.find_topics_by_name(args.substring)
        count = len(topics)
        
        print(f'Topics found: {count}')
        if count > 0:
            print('    Id  Posts  Name')
        for topic in topics:
            print(f'{topic.id:6d}  {topic.message_count:5d}  {topic.name}')
    
    if args.message:
        messages = lfdb.find_messages_by_text(args.substring)
        count = len(messages)
        
        print(f'Messages found: {count}')
        if count > 0:
            print('     Id     Date      Topic     Author\n')
        for message in messages:
            print(f'{message.id:7d}  {message.time[:10]}  {message.topic_id:6d}  {message.author_id or 0:5d}  {message.author_name or ""}')
            print(message.text)
            print()
