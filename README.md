A filter middleware for EFB
==============
A filter middleware for EFB can help you only receive messages from persons and groups you want.

Install
-----------------
install using pip3:
```
pip3 install git+https://github.com/Zerorigin/efb-filter-middleware
```

Configuration
-----------------
The config files is located in ``~\.ehforwarderbot\profiles\default\zerorigin.filter\config.yaml``.

This is a simple configuration example:
```
version: 0.1
match_mode: fuzz
strict_mode: no

work_filters:
  - black_groups
  - black_persons
  - white_groups
  - white_persons


black_persons:
  - 老黑
  - 老黄

black_persons:
  - enemy

white_groups:
  - family

white_persons:
  - john
  - jack
  - You
  - 李白

```


``version`` is used to monitor configuration change in runtime, it must be changed when changing the configuration. It is a ``float`` number.


There are four different ``work_filter``:
```
  - black_persons
  - white_persons
  - black_groups
  - white_groups
```


``white_persons`` means the persons you want to receive messages from.

``white_groups`` means groups you want to receive from.


There are two matching mode:
```
match_mode: fuzz
match_mode: exact
```
``fuzz`` This match pattern is a substring matching, which means if you have ``jack`` in your ``white_persons`` setting, ``jackson`` is also matched.

``exact`` This match pattern only matches when the whole word is the same.


There are two matching level:
```
strict_mode: yes
strict_mode: no
```
``strict_mode: yes`` means: Accept messages only if both whitelist and blacklist meet the requirements.

``strict_mode: no`` means: If one of the requirements is met, the messages is accepted.


Notice
-----------------
- Case sensitive
- All messages from you will be forwarded.


TODO
-----
