RANDOM PASSWORD MANAGER
=======================

LINUX AND MAC ONLY

INSTRUCTIONS
------------
```sh
$ cd $HOME
$ git clone https://github.com/rodrev/random-password-manager.git
$ sudo chown -R root:root $HOME/random-password-manager
```
- to run:
	`sudo python3 $HOME/random-password-manager/rpm.py`

- to run as simple command:
	`echo "alias rpm='sudo python3 $HOME/random-password-manager/rpm.py'" >> $HOME/.bashrc`
	- restart terminal. then enter:
	`rpm`
```

# NOTE:
	* Creates two gdbm database files (as bytecode - not plain text)
	using the `shelve` module of the standard python library.

	*opt* stores OPTIONS (email addresses, usernames & preferences). Rename on line 53.
	*dat* stores DATA.                                               Rename on line 54.

# SECURITY:
	* ENCRYPT this file and its directory.

	* BACKUP this file and its directory regularly onto a separate drive.
	
	* To `delete all` please delete the data file:
	`sudo rm $HOME/random-password-manager/dat`
	(new data file created next time you make an entry from the main menu)
	
	* QUIT when you're done. It starts quickly!

# SEPARATE WORK FROM PERSONAL PASSWORDS:
	Install again (as above) and rename directory to random-password-manager-work.
	New OPTIONS and DATA will be generated and treated seperately.

# FEEDBACK WELCOME.
	Version 2 if in demand.
	Bugs: roddiereventar@live.ca
	Enjoy!
