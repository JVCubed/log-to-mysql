# ssh log

#  pip dependencies:
- tailhead
- mysql-connector-python
- maxminddb
- maxminddb-geolite2

Install with the next one-liner:
python -m pip install tailhead mysql-connector-python maxminddb maxminddb-geolite2

#  SQL user
Advised is a low privilage SQL user that only can insert new lines.
```
CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';
GRANT INSERT ON log.ssh TO 'username'@'localhost';
FLUSH PRIVILEGES;
```

#  run logSSH.py
run to see if everything is fine and running without error
this should generate a CLI output.
when this runs fine you can create a service for this.

## Attributions:
This product includes GeoLite2 data created by MaxMind, available from
<a href="https://www.maxmind.com">https://www.maxmind.com</a>.
