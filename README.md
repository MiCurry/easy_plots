

# 1 Installing
1. Install Docker through
2/ Install Requirements
```
pip install -y requirements
```

3. Edit the .config file in this directory to point to the absolute path to the
media folder within this directory. This way docker can save files to the sub-
folder

For Windows and MacOS you need to make sure your directory is somewhere within
your user directory:

For Windows:
```
`//c/Users/[username]/<path-to-easy-plots>/media
```

For MacOS
```
/Users/<path-to-easy-plots>/media
```

For Linux/OSX. Do as yee wish!

4. Build the Docker image.
Build the Docker image by running. This will take some time. Let me know if
there's any errors..
```
docker -t basemap .
```

# 2 Running
* Create plots by running (args in <> will have default values):
```
python main.py plot <date> <time> <slice> <filename>
```
