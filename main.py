import praw, d20

with open('VERSION') as version:
    VERSION = version.read()

reddit = praw.Reddit('bot', user_agent='diceroll by /u/pawptart v{}'.format(VERSION))
stream = praw.models.util.stream_generator(reddit.inbox.mentions, skip_existing=True)

PREFIXES = ['!'] # more can be added as required
COMMAND = 'roll'
MENTION = '/u/DiceBagBot'
MESSAGE = "^(Want to roll your own? Mention me in a comment!)"

def format_response(result, mention):
    author_username = '/u/' + mention.author.name

    return '\n\n'.join([str(result) + ' ' + author_username, '*****', MESSAGE])

def process_roll(roll, mention):
    result = d20.roll(roll)
    response = format_response(result, mention)

    mention.reply(response)

def parse_command(mention):
    for prefix in PREFIXES:
        if COMMAND + prefix in mention.body:
            return COMMAND + prefix
        elif prefix + COMMAND in mention.body:
            return prefix + COMMAND

    return None

for mention in stream:
    command = parse_command(mention)

    if not command:
        continue

    roll = mention.body.replace(command, '').strip()
    roll = mention.body.replace(MENTION, '').strip()

    process_roll(roll, mention)
