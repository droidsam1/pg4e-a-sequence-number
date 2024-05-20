import itertools
import psycopg2
import hidden

# Load the secrets
secrets = hidden.secrets()

# Connect to the database
conn = psycopg2.connect(host=secrets['host'],
                        port=secrets['port'],
                        database=secrets['database'],
                        user=secrets['user'],
                        password=secrets['pass'],
                        connect_timeout=3)
# Create a cursor
cur = conn.cursor()

# create a pseud random stream as instructed
def pseudo_random(until):
  number = 459352
  gen = ((i + 1, int((number := int((number * 22) / 7) % 1000000))) for i in
         itertools.count(1))
  return itertools.chain([(1, number)], itertools.islice(gen, until - 1))


for value in pseudo_random(300):
  print('Inserting the tuple, ' + str(value))
  sql = 'INSERT INTO pythonseq (iter, val) VALUES (%s,%s);'
  cur.execute(sql, (value[0], value[1],))
  if value[0] % 100 == 0:
    print('Commiting')
    conn.commit()

print('Exiting program and performing final commit')
conn.commit()
