#Apollo Source Organizer

Apollo Source Organizer is a software conceived to work alongside git. It comes
to solve a problem which students have when they need to organize their homework,
as well as other people which need to manage several pieces of code which are
not related to each other. Currently, there is integration with the
[UVa Online Judge](https://uva.onlinejudge.org), which provides a wide range of programming
problems to solve.

##Concepts
The software work with some simple concepts which need to be understood in order
to operate it correclty.

- **Problem**: The problem is the entity which is related to some actual problem
available at [UVa Online Judge](https://uva.onlinejudge.org).
- **Problem attempt**: A problem can be attempted one or more times, a good practice
is to keep attempts where the problem failed in order to keep a progression log
for future study.
- **Category**: For organization purposes problems can be categorized.
- **Status**: Currently, a problem attempt can have the status of: **Working**,
**Finished**, **Archived**, and **Paused**. There also a special status of
**Temporary**. Each status represent a directory into the repository tree. **Don't
move, copy, or delete** the files manually, that's why this software was developed!
The statuses' names speak for themselves, but an brief explanation will be given
further.
- **Language**: The programming language which the attempt is being tried.

##Commands
This section explain what is done to your file tree when a command is executed.
For information about parameters type **help** or **<command> --help**.

####Create
Creates a problem attempt with the **working** status. Three files will be created:
one with the extension of the language chosen and other two with **in** and **out**
extensions, respectively.

####Pause, Finish, Archive
The problem attempt is marked as the status of the command. All of its files are
moved to the respective directory. The source files must not be edited in this mode.

####Work
A problem attempt is marked with the status of **working**. All of its files are
moved to working directory and the environment variable current problem is set
to it. If there is any working problem, it is marked as **paused**.

####Delete
The problem attempt will be deleted. All of its files will be removed from the
file tree.

####Commit
Call the **git commit** command with all the logs since the last commit. All of
the commands above have their actions registered on a log table.

####Create, Delete, Update Category
Creates, Deletes and Updates a category. Used only for organization purposes, makes
no difference on the directory tree.

####Set default category
This command set an environment variable with a category, which can be used later
as default parameters for commands which need the category.

##Updates

Always check the lastest version at [thyago.com](https://www.thyago.com).

##Requirements and Instalation

The software was developed totally using Python 3. No additional packaged are
required.

There is no installation needed. Place the scripts folder wherever is convenient
and execute it as the Execution session says.

##Execution

Execute it as:

    python3 apollo

##Licensing

See the file called LICENSE.
