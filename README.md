# dash-pimote

Use an Amazon Dash button to trigger Energenie's PiMote to remotely control any electrical device connected. The script is not limited to triggering PiMote sockets, as it can be used to trigger any two functions!

## Setup
Before you start, please ensure you add your Amazon Dash Button's MAC address in the `dash-pimote.py` file. This should be in lowercase. Details on how to find out your MAC address can be found [here](https://www.raspberrypi.org/magpi/hack-amazon-dash-button-raspberry-pi/).

## Running
Due to the GPIO being used, you need to run this script as `root` - i.e.:

```bash
sudo python dash-pimote.py
```

By default, this script will trigger all PiMote sockets paired with the PiMote Raspberry Pi accessory, but controlling individual sockets is as simple as changing the `both_on()` and `both_off()` functions accordingly. More information on using the PiMote sockets can be found [here](https://energenie4u.co.uk/res/pdfs/ENER314%20UM.pdf) and example code can be found on the Energenie website [here](https://energenie4u.co.uk/catalogue/download_software/ENER002-2PI.py).

### Thanks to:
Special thanks to [OyaMist Aeroponics](https://raspberrypi.stackexchange.com/users/86858/oyamist-aeroponics) on Raspberry Pi Stack Exchange for their assistance with this --> https://github.com/oyamist   
