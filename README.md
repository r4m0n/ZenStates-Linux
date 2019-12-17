> **If you are looking for a fix regarding random freezes using an AMD Ryzen CPU while idle (mostly Linux - Windows is always busy..) then try fixing it via BIOS settings: CPU/Zen Options in BIOS - "Power Supply Idle Control" or "Global C-state Control" should be set to `Typical current idle` (previous value `Auto` or `Low current idle`.**
> Sources: [bugzilla.kernel.org](https://bugzilla.kernel.org/show_bug.cgi?id=196683#c194), [Reddit thread](https://www.reddit.com/r/Amd/comments/cik3q1/can_we_recognize_broken_c6_states_in_all_of_zen/)


# ZenStates-Linux
Collection of utilities for Ryzen processors and motherboards

## zenstates.py
Dynamically edit AMD Ryzen processor P-States

Requires root access and the msr kernel module loaded (just run "modprobe msr" as root).

    usage: zenstates.py [-h] [-l] [-p {0,1,2,3,4,5,6,7}] [--enable] [--disable] [-f FID] [-d DID] [-v VID]

    Sets P-States for Ryzen processors

    optional arguments:
      -h, --help            show this help message and exit
      -l, --list            List all P-States
      -p {0,1,2,3,4,5,6,7}, --pstate {0,1,2,3,4,5,6,7}
                            P-State to set
      --enable              Enable P-State
      --disable             Disable P-State
      -f FID, --fid FID     FID to set (in hex)
      -d DID, --did DID     DID to set (in hex)
      -v VID, --vid VID     VID to set (in hex)
      --c6-enable           Enable C-State C6
      --c6-disable          Disable C-State C6


## togglecode.py
Turns on/off the Q-Code display on ASUS Crosshair VI Hero motherboards (and other boards with a compatible Super I/O chip)

Requires root access and the portio python module (to install run "pip install portio")
