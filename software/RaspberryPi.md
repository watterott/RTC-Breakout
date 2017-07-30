# RTC-Breakout using with Raspberry Pi

## Installation
* Open the file ```/boot/config.txt``` and add the following line at the file end:
    ```
    $ sudo nano /boot/config.txt
    ```
    ```
    dtoverlay=i2c-rtc,pcf8523
    ```

* Deactivate fake-hwclock:
    ```
    $ sudo apt-get remove fake-hwclock
    $ sudo update-rc.d -f fake-hwclock remove
    $ sudo rm /etc/cron.hourly/fake-hwclock
    $ sudo rm /etc/init.d/fake-hwclock
    ```

* Reboot the system:
    ```
    $ sudo reboot
    ```

* Known Issue:
    If the time is not set correctly on Raspbian Wheezy you have to edit the file ```/lib/udev/hwclock-set``` and change the two occurrences of ```--systz``` to ```--hctosys```.
    Further infos [here](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=764552).
    ```
    $ sudo nano /lib/udev/hwclock-set
    ```


## Using
* Show system time:
    ```
    $ date
    ```

* Show RTC time:
    ```
    $ sudo hwclock --show
    ```

* Set system time to RTC:
    ```
    $ sudo hwclock --systohc
    ```

* Set RTC time to system:
    ```
    $ sudo hwclock --hctosys
    ```
