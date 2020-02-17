# otto
Automated Herb Garden

Designed and tested solely on a Raspberry Pi 3B+. Probably easily portable to
similar devices.

# TODOs
* Gracefully detect when there's no i2c controller


# Running
From the top-level directory:

```
./src/build_and_run.sh
```

This takes care of installing dependencies and running everything. Note: it
will fail if the computer is not connected to an i2c controller.

# Dependencies

* `virtualenv`:
```
sudo apt-get install virtualenv
```

* `protoc`:
```
sudo apt install protobuf-compiler
```

# TODO(sam): Description & images
