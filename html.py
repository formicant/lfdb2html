from typing import Iterable
from data import Message

def format_page(title: str, messages: Iterable[Message]) -> str:
    return _page_template.format(
        title=title,
        message_list=''.join(_format_message(message) for message in messages)
    )


def _format_message(message: Message) -> str:
    return _message_template.format(**vars(message))


_page_template = '''
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    body {{
      font-family: Cambria, serif;
      font-size: 17px;
    }}
    header {{
      font-size: 1.5em;
      margin-bottom: 1em;
    }}
    .quoteheader a {{
      color: #444;
    }}
    blockquote {{
      margin: 0 0 0.5em;
      padding: 0.5em 1em;
      background: rgba(0, 0, 0, 0.05);
    }}
  </style>
</head>
<body>
  <header>{title}</header>
  <main>
    {message_list}
  </main>
</body>
</html>
'''

_message_template = '''
    <div class="message">
      <div class="quoteheader">
        <a href="https://lingvoforum.net/index.php?topic={topic_id}.msg{id}#msg{id}">
          {author_name}, {time}
        </a>
      </div>
      <blockquote>
        {text}
      </blockquote>
    </div>
'''
