# Inputs, Outputs, and Syncing

### Input columns:
Please fill out only required info for each radio channel.
Leave unused fields blank. Filling additional columns may cause
unpredictable behavior.

At the moment, all fields are case-sensitive.

| **Column Name** | Description |
|---|---|
|number|The sequence in your radio, starts at 1.|
|name|What you would like to call your channel, unlimited characters|
|medium name| Name (truncated to 8 characters) `FFO ElDorado -> FFO Eldo`
|short name| Name (truncated to 7 characters) `FFO Eldorado -> FFO ELD`
|group id| Channel preset group ID |
|rx freq| Receive frequency |
|rx ctcss| Receive PL tone |
|rx dcs | Receive DCS code |
|rx dcs invert |  `True` or `False` if your tx DCS code is inverted |
|tx offset| Difference from receive channel, in MHz ex:`0.6` |
|tx ctcss | Transmit PL tone|
|tx dcs invert | `True` or `False` if your tx DCS code is inverted |
|digital timeslot | DMR Timeslot, should be either 1 or 2 |
|digital color | Color parameter of DMR channel |
|tx power| Low, Medium, High |

### Yaesu FTM-400
This is the "RT Systems" branded sync software.

1. Clear channels in existing image before importing
1. Import ftm400.csv, all columns, do not exclude rows
1. "Step" will default to 5kHz. This is an error on their end
1. Final user touchup.

### Baofengs
1. Import your radio's image.
1. Clear all rows.
1. Import baofeng.csv
1. Final user touchup.

***
# Known radio issues:

###All radios:
* Unparseable fields may case an application crash.
###FTM400: 
* The `step` column is not parsed correctly by the RT app.
###Baofeng:
* `power` column does not sync.
