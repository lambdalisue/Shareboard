Shareboard
=============================================================================

Shareboard is a local HTTP server which works like clipboard.
After you start the server, you can simply set/get the text data to that
server with HTTP communication. It is useful to connect two different process.

Shareboard also give you a builtin HTTP viewer to display the data. You can
use this HTTP viewer to visualize your HTML text.


Install
-----------------------------------------------------------------------------
Use [easy_install][] or [pip][] to install. Follow the command below

    $ easy_install shareboard

or

    $ pip install shareboard

[easy_install]: http://packages.python.org/distribute/easy_install.html
[pip]: http://pypi.python.org/pypi/pip


Usage
-----------------------------------------------------------------------------

### Clipboard

The basic mechanisms of Shareboard is described below. Shareboard use HTTP
connection to set/get text data.

    Sender === POST: http://localhost:8081/ ==> Shareboard
    Getter <== GET : http://localhost:8081/ === Shareboard

As I described, Shareboard use local HTTP server so you must start the server
before use. You can start the server with the command below

    $ shareboard start

Shareboard provide you a small script to set/get text data so you can simply
set/get data to/from Shareboard with following commands

    $ shareboard set "Hello World"
    $ shareboard get
    Hello World

#### Clipboard advance

If you specify, Shareboard automatically run a text modification program
everytime when you set text data. For example, you can use `sed` to modify
the text data with the commands below

    $ shareboard start -c 'sed "s/Hello/Hi/g"'

With this shareboard server, data will be modified with the command like below

    $ shareboard set "Hello World"
    $ shareboard get
    Hi World

### Builtin HTML viewer

Shareboard is developed to help a program such as a Markup viewer for vim.
That's why it has builtin HTML viewer written in Qt.
To enable this feature, you have to install the following libraries

-   [Qt](http://qt-project.org/)
-   [PySide](http://qt-project.org/wiki/PySide)

After you install these libraries, simply start the Shareboard server with
`-v` option like

    $ shareboard start -v
    
The builtin HTML viewer will automatically be refreshed everytime when you set
new text data.

Special thanks
-----------------------------------------------------------------------------

Shareboard is originally inspired by
[mkdpreview](https://github.com/mattn/mkdpreview-vim).
