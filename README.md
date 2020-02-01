# CityScoPy

### [=> Download latest release <=](https://github.com/CityScope/CS_Scanner_Python/releases/)

#### A tool for bootstrapping, scanning and networking MIT CityScope Projects in Python

CityScoPy is the main component of an interactive MIT CityScope table.
It is used for initiating and later run a interactive CityScope instance in any arbitrary geolocated area in the world. CityScoPy can capture, key-stone, scan and send uniquely tagged arrays of 2-dimension physical bricks.

---

## Usage

-   install python 3.4 or higher
-   clone this repo

```
$ git clone https://github.com/CityScope/CS_CityScoPy.git
$ cd CS_CityScoPy
```

-   install packages. To produce a list of needed packages, use `pipreqs`, follow instructions https://github.com/bndr/pipreqs. Or, simply run the app and install packages as they appear in errors.
-   tweak `__settings__.json` to fit your cityIO table setup. Read [cityIO documentation](https://github.com/cityscope/cs_cityio_backend/wiki) for proper data structure
-   setup a path to your settings file

```
cityscopy_settings_path = "__path__/__settings__.json"
```

-   initiate the `Cityscopy` class (see `run.py` example)

```
cityscopy = Cityscopy(cityscopy_settings_path)
```

-   use one or more of the main methods. 'Blocking' means the method will run forever (while true loop). Advanced users can parallel blocking methods using multithreading.

| Method                     | Usage                             | Blocking? |
| -------------------------- | --------------------------------- | --------- |
| `cityscopy.keystone()`     | initial keystone and save to file | x         |
| `cityscopy.scan()`         | main scanning and sending method  | x         |
| `cityscopy.udp_listener()` | emulate local UDP server listener | x         |

-   in terminal run the tool using `$ run.py`

---

## Class methods

### `Cityscopy.keystone()`

##### Initial keystone and save to file

-   the tool will start given a cam is connected and working
-   Select 4 corners [up right, up left, bottom right, bottom left, at this order] of keystone region
    Note: no need to exactly select the corners, as these are only initial guides for `scanner` method
-   `keystone.txt` and close

### `Cityscopy.scan()`

##### main scanning and sending method

Scanner will detect colors in arrays of 2d-pixel arrays. Than, these color arrays will be compared to list of `tags` attribute of a given `__settings__.json` file. Then the tool will return a list of `type` and `rotation` for each of the scanned arrays. This list is then converted to cityIO acceptable JSON format and can be sent using POST request.

##### options in `__settings__.json`

-   `gui` turn on or of webcam display
-   `interval` send rate to UDP/HTTP in ms
-   `cityio` send to UDP or HTTP cityIO
-   `tags` 16 digit strings of types being scanned [`1000000100000000`]

Tool will start scanning using whatever keystone data was stored in `keystone.txt`
make corrections to the key stone using the sliders or keyboard using `1,2,3,4` to select a corner and `[w,a,s,d]` to move `[up,left,down,right]` the selected corner. Press `k` to save change to file and `ctrl-c` twice [in the terminal window] to exit program

### `Cityscopy.udp_listener()`

##### emulates local UDP server listener

## Errors

OS, Python versions, openCV and peripheral devices such as webcams can sometimes cause issues. If you found and issue, please report it as a Github issue. Here're some encountered issues and their solutions:

-   Mac OSX High Sierra blocks multithreading

    -   issue: `objc[67570]: +[__NSPlaceholderDate initialize] may have been in progress in another thread when fork() was called.`
    -   solution: add to your `$ .bash_profile` the line `export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`. See more here: https://stackoverflow.com/questions/50168647/multiprocessing-causes-python-to-crash-and-gives-an-error-may-have-been-in-progr

-   Webcam crash on init, despite working on other apps
    -   issue: camera is not configured in `settings.json`
    -   solution: make sure to test different `camId` values. Your OS might put the camera after another device (2,3..)

---

## License

Please see `LICENSE` file for more details.This tool may require libraries which are subject to own licensing.

## Contribution

Please use GitHub Issues and PR interface for contributions.

---

Maintained by [Ariel Noyman](http://arielnoyman.com)

[Repo contributors](https://github.com/CityScope/CS_Scanner_Python/graphs/contributors)
