


# Todo
1. download
2. plot-2d
3. Html


# Installing
1. Clone this repository. If you're on Windows or MacOS make sure you clone it somewhere
in a user folder
(Windows: ://C/users/username/easy_plots, MacOS:/Users/easy_plots/media).
```
git clone https://github.com/MiCurry/easy_plots.git
```

2. Install Docker if you haven't.

3. Build the Docker image by running. This will take some time. Let me know if
there's any errors..
```
docker -t basemap .
```

# Running
1. Mount Point
Before you start running you'll need to pick a mount directory so the Docker
container can create a data volume to save files it downloads and plots it
saves as well as allowing you to see plots it creates.

This mount directory needs to point to the directory *data* contained within
this repository. You'll need to remember this direcotry path (best to write it
down). Mine is `//c/users/miles/projects/easy_plots/data`.

2. Create plots by using the docker run command and mounting the volume. You'll
use this volume each time you want to plot! Make sure you use it each time else
you wont be using the data you've already generated.

The basic structure of the run command is:
```
docker run -v [your-mount-direcotyr]:/home/data basemap <command>
```

Here's mine as an example:
```
docker run -v //c/user/miles/projects/easy_plots/nams/data:/home/NAMS/data basemap <command-line-options>
```

# Commands
