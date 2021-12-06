(Add this a the top of the 381Bot.py)
import os

(Define this anywhere in 381Bot.py)
def create_backup(incoming_msg):
    """Create Backup"""
    response = Response()
    response.text = "Creating backup....\n\n"
    global exit_flag
    exit_flag = True
    time.sleep(5)
    bashCommand = "ansible-playbook backup_cisco_router_playbook.yaml"
    os.system(bashCommand)
    response.text = "Backup created and saved to backup folder...\n\n"

    return response

(Add this line to 381Bot.py where all the other bot.add_commands are)
bot.add_command("backup", "This job will create a backup of router 1", create_backup)