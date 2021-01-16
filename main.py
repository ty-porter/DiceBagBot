import d20, praw, re, traceback

with open('VERSION') as version:
    VERSION = version.read()

reddit = praw.Reddit('bot', user_agent='DiceBagBot by /u/pawptart v{}'.format(VERSION))
stream = praw.models.util.stream_generator(reddit.inbox.mentions, skip_existing=True)

PREFIXES = ['!'] # more can be added as required
COMMAND = 'roll'
MENTION = '/u/DiceBagBot'
MESSAGE = "^(Want to roll your own? Mention me in a comment!)"
ERROR_MESSAGE = "Sorry, that command couldn't be parsed. Check out /r/DiceBagBot for syntax help."

def format_response(result, mention):
    author_username = '/u/' + mention.author.name

    return '\n\n'.join([str(result) + ' ' + author_username, '*****', MESSAGE])

def process_roll(roll, mention):
    try: 
        result = d20.roll(roll)
    except Exception:
        print('Unrecognized command, replying with error.')
        traceback.print_exc()
        mention.reply(ERROR_MESSAGE)
        return

    response = format_response(result, mention)

    print('Replying!')
    mention.reply(response)

def parse_command(mention):
    for prefix in PREFIXES:
        if COMMAND + prefix in mention.body:
            print('Found command {} in mention {}.'.format(COMMAND + prefix, mention.id))
            return COMMAND + prefix
        elif prefix + COMMAND in mention.body:
            print('Found command {} in mention {}.'.format(prefix + COMMAND, mention.id))
            return prefix + COMMAND

    return None

for mention in stream:
    print('Mentioned! Comment {} by /u/{}.'.format(mention.id, mention.author.name))
    command = parse_command(mention)

    if not command:
        print('Command not found, skipping {}.'.format(mention.id))
        continue

    roll = mention.body.replace(command, '').strip()
    roll = roll.replace(MENTION, '').strip()

    print('Processing the command...')
    process_roll(roll, mention)
    print('Done!')
