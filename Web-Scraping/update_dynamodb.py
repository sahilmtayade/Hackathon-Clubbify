import boto3
import pandas as pd

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Instantiate a table resource object without actually
# creating a DynamoDB table. Note that the attributes of this table
# are lazy-loaded: a request is not made nor are the attribute
# values populated until the attributes
# on the table resource are accessed or its load() method is called.
table = dynamodb.Table('clubs')

# Print out some data about the table.
# This will cause a request to be made to DynamoDB and its attribute
# values will be set based on the response.
print(table.creation_date_time)
df = pd.read_csv("./Web-Scraping/club_data.csv")
with table.batch_writer(overwrite_by_pkeys=['club_name', 'day']) as batch:
    for index, row in df.iterrows():
        name, day, time, statement, topics = row[1:]
        pre = topics[1:-1].split(', ')
        pre = [p[1:-1] for p in pre]
        topics = set(pre)
        batch.put_item(
            Item={
                'club_name': name.lower(),
                'day': day,
                'statement': statement,
                'time': time,
                'topics': topics
            }
        )