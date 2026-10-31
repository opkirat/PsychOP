import json
from datetime import datetime
import re

data_dict = {}
i = 0


with open("data/dubey.txt") as f:
    for line in f:
        line = line.strip() # Strip whitespace

        if " (Read by" in line:
            line = line.split(" (Read by")[0]  

        try:
            date = datetime.strptime(line, '%b %d, %Y %I:%M:%S %p')
            sender = next(f).strip()
            next_line = next(f).strip()

            ## Reactions to messages
            reaction = "no"
            reaction_emotion = ""
            reacted_by = ""

            ## Messages
            message = ""
            pattern = r"^[A-Z][a-z]{2} \d{1,2}, \d{4}\s+\d{1,2}:\d{2}:\d{2} (?:AM|PM)(?: \(Read by.*\))?$"
            
            while next_line != "" and not re.fullmatch(pattern, next_line.strip()):
                if next_line.startswith("Edited ") and " later:" in next_line:
                    message = next_line.split(" later:", 1)[1].strip()

                elif next_line.startswith("Tapbacks:"):
                    reaction = "yes"
                    next_line = next(f, "").strip()
                    reaction_emotion = reaction_emotion + next_line.split(" by ", 1)[0]
                    reacted_by = reacted_by + next_line.split(" by ", 1)[1]
                    
                else:
                    message = message + next_line + "\n"    
                next_line = next(f, "").strip()
    
            print(f"Sent Date: {date}")
            print(f"Sent By: {sender}")
            print(f"Message: {message}")
            print(f"Reaction: {reaction}")
            print(f"Reaction Emotoin: {reaction_emotion}")
            print(f"Reacted By: {reacted_by}")

            ## Create our dictionary
            data_dict[i] = {
                "date": date,
                "sender": sender,
                "message": message,
                "reaction": reaction,
                "reaction emotion": reaction_emotion,
                "reacted by": reacted_by
            }
            i = i + 1

        except ValueError:
            pass

with open("data/messages.json", "w", encoding="utf-8") as f:
    json.dump(data_dict, f, indent=4, ensure_ascii=False, default=str)