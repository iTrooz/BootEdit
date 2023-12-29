# BootEdit


Modify UEFI entries directly from your OS !
Supported platform: Linux and Windows. Interested in MacOS of someone wants to contribute it

# Features
- move entries 
- add a new entry
    - select partition manually
    - select file manually
- delete an entry
# Not done features
- Findind bootable files automatically ("Find .. file" buttons)

# Contribute

I use poetry to manage my environement. These commands should get you started:
```sh
poetry init # create environment and 
poetry shell # enter environement
sudo -E bash # elevate as root (but stay in the enviroment)
python main.py # run app
```

# Screenshots

![image](https://user-images.githubusercontent.com/42669835/251552608-3edfd45b-ef23-49a9-9d46-335d9825bc50.png)

# Disclaimer

This program is offered AS IS, WITHOUT ANY GUARANTY.
Any failure from the software and any damage it could cause (for example, but not limited to, not being able to boot because the boot order is messed up) are your responsibilites, and not the developer's.
