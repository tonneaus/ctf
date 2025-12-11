![](delicious\_cooking.png)

We're given a sqlite database and a username.  Let's open the
database in `sqlite3` and see what tables there are.

```
$ sqlite3 
sqlite> .schema
CREATE TABLE users(username PRIMARY KEY, password, security_q);
```

Let's look at our user.

```sql
select * from users where username = 'meatballfan19274';
```
```
meatballfan19274|09be2259e0224f41b96b633b73e7138b50b4be0a1ae20c0eb6a7434e8fc47303$334aa758c52bb2f862f1607ff098e954|I refuse to use security questions for security reasons
```

The `password` field is made up of two hex strings separated by `$`.
The first hex string represents 32 bytes, so maybe it's a SHA-256
digest. The next part is 16 bytes, and if it's being stored with a
hash, it's probably a salt.

The database reuses salts.  It also stores password hints (in
the column "`security_q`").  This means we can list all password hints for a given password.

```sql
select distinct security_q from users where password = (select password from users where username = 'meatballfan19274');
```
```
I refuse to use security questions for security reasons
Change is nature, dad
Anyone can cook
White not everyone can be a great artist, a great artist can come form anywhere
One can get too familiar with vegetables, you know
look at the post-it note on your desk
password manager!
eggselent password
foodXXXX
i'm hungry
fav movie + bank pin
```

The password is probably related to some movie about food. Let's
google one of the quotes:

![](quote.png)

The hint `fav movie + bank pin` reveals the format of the password.
Bank PINs are usually 4 digits.  With this we're ready to brute
force the password.

```py
import hashlib

DIGEST = bytes.fromhex('09be2259e0224f41b96b633b73e7138b50b4be0a1ae20c0eb6a7434e8fc47303')
SALT = bytes.fromhex('334aa758c52bb2f862f1607ff098e954')

for movie in ('Ratatouille', 'ratatouille'):
    for i in range(10000):
        pw = movie + f'{i:04}'
        if DIGEST in (
            hashlib.sha256(SALT + pw.encode()).digest(),
            hashlib.sha256(pw.encode() + SALT).digest(),
        ):
            print(f'VuwCTF{{{pw}}}')
            break
```        

This produces output:
```
VuwCTF{ratatouille6281}
```

## Mistakes this application made

- reusing salts
- using a fast hash function for hashing passwords
- storing password hints
