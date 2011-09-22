Minus.com API Python Library
============================

version: 0.1 (alpha)

This is the initial and unstable version of Minus.com Python Library.

Minus.com is the easiest way to share files online for free. Drag files onto 
our site or use our desktop and mobile applications. Get 10 GB of Free Space to
start sharing today.

Objects
-------

3 dictionary like Minus API objects:
 * User
 * Folder
 * File

Lists
-----

Some interfaces return a list of objects:
 * UserList
 * FolderList
 * FileList


Examples
--------

Authenticate::

    from minus import Minus
    m = Minus('==== access key ====', 'https://minus.com/api/v2')

Get active User::

    user = m.get_activeuser()

Get folders of user::

    folder_list = user.get_folders()

Get a folder from folder_list::
    
    folder = folder_list[0]

Iterate through list::
    
    for folder in folder_list:
        print folder['name']

Create a directory::
    
    new_folder = user.create_folder('Test', False)

Upload a file::
   
    file_obj = open('test.jpg', 'rb')
    new_file = new_folder.add_file(file_obj, 'test.jpg', 'Test!!')


  

