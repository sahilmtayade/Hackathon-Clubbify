days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
ans = ""
d = []
for day in days:
    for i in range(len(day)-4):
        ans+= day[:i+1] + '|'
    d.append(day[:-3])
print(f"(?:(?:{ans[:-1]})")
print('|')
print(f"(?:{'|'.join(d)})(?:d|da|day)?)\s?")

# Regex: (?:^|\s)((?:(?:M|Mo|T|Tu|Tue|W|We|Wed|Wedn|Wedne|T|Th|Thu|Thur|F|Fr|S|Sa|Sat|Satu|S|Su)|(?:Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)(?:d|da|day)?)s?)\.?,?\s*?(?:@|at)?\s?(\d{1,2}:?(?:\d{2})?)\s?(pm|am)?
# REEEgex: (?:^|\s)((?:(?:M|Mo|T|Tu|Tue|W|We|Wed|Wedn|Wedne|T|Th|Thu|Thur|F|Fr|S|Sa|Sat|Satu|S|Su)|(?:Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)(?:d|da|day)?)s?)\.?,?\s*?(?:@|at)?\s?(\d{3,4}|(?:\d{1,2}:?(?:\d{2})?))\s?(pm|am)?