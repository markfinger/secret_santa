import random
import smtplib
import time
from settings import people, couples, email, from_addr


# Make the couple exclusions two-way for easy dict lookups
for person in couples.keys():
    couples[couples[person]] = person

# Match people up
possible_recipients = people.keys()
pairings = {}
for name in people.keys():
    recipient = None
    # Sample until the recipient is neither themselves nor their partner
    while recipient in (None, name, couples.get(name, None)):
        recipient = random.choice(possible_recipients)
    possible_recipients.remove(recipient)
    pairings[name] = recipient

# Email each person
for name, recipient in pairings.iteritems():
    to_addrs = people[name]
    msg = '{0}, your secret santa recipient is {1}.'.format(name, recipient)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(email['username'], email['password'])
    server.sendmail(from_addr, to_addrs, msg)
    server.quit()

    # Try not to anger the Gods o' Spam
    print 'Sent to ' + to_addrs
    time.sleep(5)