# otto
Automated Herb Garden

Designed and tested solely on a Raspberry Pi 3B+. Probably easily portable to
similar devices.

# TODOs
* Gracefully detect when there's no i2c controller


# Running
From the top-level directory:

```
ln -s /etc/systemd/system/otto.service /home/pi/otto/otto.service
sudo systemctl daemon-reload
sudo systemctl enable otto.service
sudo systemctl start otto.service
```

If it's the first time running the binary on the machine, better to do:

```
./src/build_and_run.sh
```

This takes care of installing dependencies and running everything. Note: it
will fail if the computer is not connected to an i2c controller.

# Dependencies

* [i2c Support](https://www.waveshare.com/wiki/Raspberry_Pi_Tutorial_Series:_I2C)

* `virtualenv`:
```
sudo apt-get install virtualenv
```

* `protoc`:
```
sudo apt install protobuf-compiler
```

* `i2c-tools`:
```
sudo apt install i2c-tools
```


# TODO(sam): Description & images
