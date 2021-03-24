# Inputs, Outputs, and Syncing

### Input columns:
Please fill out only required info for each radio channel.
Leave unused fields blank. Filling additional columns may cause
unpredictable behavior.

At the moment, all fields are case-sensitive and all csv's are required.

### input.csv
| **Column Name** | Description |
|---|---|
|number|The sequence in your radio, starts at 1.|
|name|What you would like to call your channel, unlimited characters|
|medium_name| Name (truncated to 8 characters) `FFO ElDorado -> FFO Eldo`
|short_name| Name (truncated to 7 characters) `FFO Eldorado -> FFO ELD`
|zone_id| Channel preset zone ID |
|rx_freq| Receive frequency |
|rx_ctcss| Receive PL tone |
|rx_dcs | Receive DCS code |
|rx_dcs_invert |  `True` or `False` if your tx DCS code is inverted |
|tx power| Low, Medium, High transmit power |
|tx_offset| Difference from receive channel, in MHz ex:`0.6` |
|tx_ctcss | Transmit PL tone|
|tx_dcs_invert | `True` or `False` if your tx DCS code is inverted |
|digital_timeslot | DMR Timeslot, should be either 1 or 2 |
|digital_color | Color parameter of DMR channel |
|digital_contact_id | Contact to call on DMR channel |
### zones.csv
| **Column Name** | Description |
|---|---|
|number| Number of the zone, starting at 1|
|name| Zone name |
### dmr_id.csv
| **Column Name** | Description |
|---|---|
|number | number of DMR ID, starting at 1|
|radio_id | ID number from radioid.net
|name | nickname of DMR ID|
### digital_contacts.csv
| **Column Name** | Description |
|---|---|
|number|Number of talkgroup/zone, starting at 1|
|digital_id|Talkgroup or contact ID|
|name|Name of contact|
|call_type|Either `group` or `all`

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

### Anytone 878
1. Create/open your rdt file.
1. Import Channel, Radio ID List, Zone, Talk Groups CSVs
1. Final user touchup

***
# Known radio issues:
### FTM400: 
* The `step` column is not parsed correctly by the RT app.
### Baofeng:
* `power` column does not sync.
### Anytone 878:
* Talkaround not supported.
