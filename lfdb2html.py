import re
from argparse import ArgumentParser
from lfdb import LfDb
from html import format_page

default_db_file = 'lfdb_2021-11-16.sqlite'

parser = ArgumentParser(description='Creates an HTML file containing all the messages of a given user or topic.')

what_to_find = parser.add_mutually_exclusive_group(required=True)
what_to_find.add_argument('-u', '--user', action='store_true', help='User messages')
what_to_find.add_argument('-t', '--topic', action='store_true', help='Topic messages')

how_to_identify = parser.add_mutually_exclusive_group(required=True)
how_to_identify.add_argument('-i', '--id', help='User/topic ID')
how_to_identify.add_argument('-n', '--name', help='User/topic name')

parser.add_argument('-o', '--output', help=f'Output HTML file')
parser.add_argument('-d', '--database', help=f'Sqlite database file. ("{default_db_file}" is used by default)')

args = parser.parse_args()

db_file = args.database or default_db_file


with LfDb(db_file) as lfdb:
    
    if args.user:
        if args.id is not None:
            id = int(args.id)
            user = lfdb.get_user_by_id(id)
        else:
            user = lfdb.get_user_by_name(args.name)
        
        if user is not None:
            title = f'user{user.id} {user.name}'
            messages = lfdb.get_user_messages(user.id)
        else:
            raise LookupError('Cannot find the user!')
    
    else:
        if args.id is not None:
            id = int(args.id)
            topic = lfdb.get_topic_by_id(id)
        else:
            topic = lfdb.get_topic_by_name(args.name)
        
        if topic is not None:
            title = f'topic{topic.id} {topic.name}'
            messages = lfdb.get_topic_messages(topic.id)
        else:
            raise LookupError('Cannot find the topic!')
    
    if args.output is not None:
        file_name = args.output
    else:
        file_name = re.sub('[\\/|<>:?*"]', '_', title)[:60] + '.html'
    
    html = format_page(title, messages)
    
    with open(file_name, "w", encoding='utf-8') as file:
        file.write(html)
