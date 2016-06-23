Random Password Manager
=======================

***LINUX AND MAC ONLY***

# INSTALL

```
$ cd $HOME
$ git clone https://github.com/rodrev/random-password-manager.git
```


# Run

`$ sudo python3 $HOME/random-password-manager/rpm.py`

Simplify the run command:

    `$ echo "alias rpm='sudo python3 $HOME/random-password-manager/rpm.py'" >> $HOME/.bashrc`

- restart terminal. then enter:

    `$ rpm`


# NOTE

Creates two files in the random-password-manager directory.

**opt** stores OPTIONS (email addresses, usernames & preferences). *to rename edit line 53 of rpm.py*

**dat** stores DATA.                                               *to rename edit line 54 of rpm.py*

These are gdbm database files (bytecode) created using the `shelve` module of the standard python library.


# Main Menu

```
  -------------------------------
  random p.a.s.s.w.o.r.d. manager
  -------------------------------
  [1] make
  [2] enter yourself
  [3] quick
  -------------------
  [4] get
  [5] edit
  [6] delete
  -------------------
  [7] print all
  [8] change all
  -------------------
  [9] options
  [0] quit
```

Choose by number.

`1` make an entry (save a random password and info)

`2` make an entry (save your own password and info)

`3` show me a random password (don't save)

`4` get an entry (get password and info)

`5` edit an entry (change anything except its name... delete and make a new one to do that)

`6` delete an entry (type carefully)

`7` print all saved password entries to screen or to file  (Maybe you want a hard copy.  Now you need a shredder.)

`8` change all entries to new random passwords (don't do this unless you first print your old passwords)

`9` options:
	- manage email addresses
	- manage usernames
	- choose length to make random passwords
	- choose a length range (+/-) to make random passwords
	- choose to use punctuation in your passwords (except for quotes and backslashes which are trouble)

`0` save everything and exit the program


# [1] make

Creates a random password entry with a unique name.

You can also add an email address, username, and notes.

***Example session***

`Your input looks like this`

>	output looks like this

-------------------------------------

select 'make' by typing 1

`1`

names can have spaces

>	entry [name]: `Google`

>	emails:

>	0 none
	
>	[enter] default. <\*> other. <number> select:

>	`*`

>	email: `myname@gmail.com`

>	myname@gmail.com saved to your email list.

>	usernames:

>	0 none

>	[enter] default. <\*> other. <number> select:

>	`*`

>	username: `user1`

>	user1 saved to your usernames list.

>	[enter] done. note(s): `this is a note`

>	[enter] done. note(s): `this is another note`

>	[enter] done. note(s): `<enter>`


```
	Google

	myname@gmail.com

	user1

	.w+U>?UAW$bJ>Uk

	this is a note

	this is another note

```

>	saved. [enter]... `<enter`

---------------------------------------------

Done.

Back to main menu.

Your random password is printed under your username.

This time it happened to be `.w+U>?UAW$bJ>Uk`

- default random password length is 16 characters. 
	- change it to any length in ***[9] options***
- some punctuation may be used in the random password by default.
	- turn off punctuation in ***[9] options***

Exit the program by selecting ***[0] quit***


# GET YOUR PASSWORD FROM THE SHELL

What was my Google password again? Why did I log out anyway?

`$ sudo python3 $HOME/random-password-manager/rpm.py Google`

If you created the `rpm` alias as the ***Install*** suggested above...

`$ rpm Google`

```
	Google

	myname@gmail.com

	user1

	.w+U>?UAW$bJ>Uk

	this is a note

	this is another note

```

Just the password please

`$ rpm --quiet Google`

>	.w+U>?UAW$bJ>Uk


# GET YOUR PASSWORD FROM THE MAIN MENU

##	[4] get

Lists the names of your passwords to remind you.  Type a name to get its password info.  

Choose 4 from the main menu

`4`

>	names:
>	Google
--------------------------------------------

[enter] main menu. get entry [name]: `Google`

--------------------------------------------
```
Google
myname@gmail.com
user1
.w+U>?UAW$bJ>Uk
this is a note
this is another note
```


# SECURITY NOTES

ENCRYPT this file and its directory.

BACKUP this file and its directory regularly onto a separate drive.
	
To delete all entries at once please delete the data file. A new data file will be created 
the next time you make an entry from the main menu:
`sudo rm $HOME/random-password-manager/dat`

QUIT when you're done. It starts quickly!


## SEPARATE WORK FROM PERSONAL PASSWORDS

Install again and rename directory to `random-password-manager-work`.

Create another alias `rpm-work`

New OPTIONS and DATA files will be generated and treated separately within this directory.

Each installation is completely independent.


## FEEDBACK WELCOME

Send comments, feature requests, bugs to roddiereventar@live.ca

