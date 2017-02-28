import telepot
import os
import glob
from time import sleep

LAST_COMMAND = {}
training_content = 'training'


def main():
    """Main Function"""
    dict_train = load_training()

    bot = telepot.Bot(os.environ['BOT_TOKEN'])
    bot.message_loop(lambda x: check_training(x, dict_train, bot))

    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        return


def check_training(msg, dict_train, bot):
    """Event loop to check what is going on"""
    global LAST_COMMAND
    text, user_id = decrypt_msg(msg)

    if user_id in LAST_COMMAND:
        if text in dict_train['first_commands']:
            LAST_COMMAND[user_id] = [text]
            message = 'Your choice: {0}!\nContinue with week:\n{1}'.format(text, ','.join(dict_train['second_commands']))
            bot.sendMessage(user_id, message)
        elif text in dict_train['second_commands']:
            handle_second_command(text, user_id, dict_train, bot)
        elif text in dict_train['third_commands']:
            handle_third_command(text, user_id, dict_train, bot)
        elif text == '/help':
            LAST_COMMAND[user_id] = ['help']
            message = format_output(user_id, dict_train, '')
            bot.sendMessage(user_id, message)
        else:
            bot.sendMessage(user_id, 'Command not valid: {0}'.format(text))
    elif text in dict_train['first_commands']:
        LAST_COMMAND[user_id] = [text]
        message = 'Your choice: {0}!\nContinue with week:\n{1}'.format(text, ','.join(dict_train['second_commands']))
        bot.sendMessage(user_id, message)
    elif text == '/help':
        LAST_COMMAND[user_id] = ['help']
        message = format_output(user_id, dict_train, '')
        bot.sendMessage(user_id, message)
    else:
        bot.sendMessage(user_id, 'Command not valid: {0}'.format(text))


def handle_second_command(text, user_id, dict_train, bot):
    """Handle the second command case"""
    global LAST_COMMAND
    if LAST_COMMAND[user_id][-1] in dict_train['first_commands']:
        LAST_COMMAND[user_id].append(text)
        message = 'Your choice: {0}!\nContinue with day:\n{1}'.format(''.join(LAST_COMMAND[user_id]), ','.join(dict_train['third_commands']))
        bot.sendMessage(user_id, message)
    else:
        pass


def handle_third_command(text, user_id, dict_train, bot):
    """Handle the thid command case"""
    if LAST_COMMAND[user_id][-1] in dict_train['second_commands']:
        if text != '/all':
            message = format_output(user_id, dict_train, text)
            bot.sendMessage(user_id, message)
        else:
            for entry in dict_train['third_commands']:
                if entry != '/all':
                    message = format_output(user_id, dict_train, entry)
                    bot.sendMessage(user_id, message)
    else:
        pass


def format_output(user_id, dict_train, text):
    """Format the output in a nice way"""
    key = '{0}{1}'.format(''.join(LAST_COMMAND[user_id]), text)
    lines = []
    lines.append('Choice: {0}\n\n'.format(key)) 
    for idx, entry in enumerate(dict_train[key]):
        entry = entry.replace('|', '\n')
        if idx == 0:
            text = 'Type: {0}\n\n'.format(entry)
        else:
            text = '- {0}\n\n'.format(entry)
        lines.append(text)

    return ''.join(lines)


def decrypt_msg(msg):
    """Return only the important notes"""
    return msg['text'], msg['chat']['id']


def load_training():
    """Load the training from text file"""
    dict_train = {}
    for train_file in glob.glob('{0}/*'.format(training_content)):
        if train_file == '{0}/template.txt'.format(training_content):
            continue
        with open(train_file, 'r') as read:
            for line in read:
                line = line.rstrip('\n')
                if line == '':
                    continue
                if line.startswith('###'):
                    key = line.split(' ')[-1]
                else:
                    dict_train[key] = line.split(',')
    
    return dict_train


if __name__ == '__main__':
    main()

