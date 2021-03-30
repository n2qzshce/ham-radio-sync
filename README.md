# Ham Radio CSV Sync Tool for PC and OSx

**Releases: All versions can be found on the 
[releases page.](https://github.com/n2qzshce/ham-radio-sync/releases)**

### What it is
This ham radio csv tool is designed to help you create import files for different radios 
from a master list. Radios all use different formats for different fields, and
keeping these in sync is a tedious task that is prone to errors.

Currently supported radios:
* Default output: Digests the input, should expose errors
* Baofeng uploads via CHiRP
* Yaesu FTM400 via RT systems application
* Anytone D878, D868, D578 via D878UV
* Connect Systems CS-800D via Connect Systems Software
* Kenwood 71/710 Series via MCP2

### How it works
This is a command line tool that will get you setting up your radios as quickly
as possible.
1. Run the Wizard to generate the input CSVs.
2. Add your channels and configuration information to the input CSVs.
3. Select your radios and create radio plugs!
4. Import your radio plugs into your radio programming application.
5. Upload to your radio, and you're done.

##### Windows defender will warn you about opening the GUI version. Click on the `more info` dialogue to run.

### General requirements
* You may want some knowledge of how to run a command line application.
* The executable should be placed in a directory by itself. This will allow for
the `wizard` to create the necessary `in` and `out` folders.

    ##### **This program will create folders around it!**

### Command overview
* `--help` Displays a usage info page.
* `--wizard` this will create a boilerplate csv for you to start configuring, along
with the necessary directories for processing your csv's.
* `--clean` deletes the `in` and `out` folders to allow you to start over. 
**Make backups before running ** (if needed)
* `--force` This can be used in tandem with `wizard` any other command requiring yes
/ no prompts to default to "yes" for all questions.
* `--radios` The meat and potatoes, pass in a list of supported radio names to update
/ re-create your CSV files.
    * Example use: `radio_sync.exe --radios ftm400` creates a csv for a Yaesu FTM-400.
* `--debug` Adds some more output to the console, primarily for developers.

### For best results...
If you do not need a column, *leave it blank*. All radio frequencies and offsets are in
Megahertz. Do not add any units, just input the number.

Some sync applications have bugs where they cannot read certain values. You may need
to "touch up" your radio configs after they are generated.

Double-check your results before uploading your codeplug.

* [Inputs and radio sync guide](INPUTS_OUTPUTS_SYNCING.md)

### Bugs, feature requests, and support
Please create a ticket in the "issues" section of this project. Please try to provide
as much info as possible:
* Your specific app version
* What *specifically* you expected. "This cell should have been `88.0hz`"
* What *specifically* happened. "This cell had the value `88 hz`"
* For feature requests, the specific rules and information that is relevant:
    * "I would like to be able to support timezones for the FOO900D radio" (plug
    management link tool). This specific column should have a format like 
    `America/Chicago`"

 If possible, please attach your `input.csv` to the ticket so your issue can be
 resolved quickly.
 
### My radio/app isn't supported!
If you have a radio or app that isn't supported, please create a ticket with as much
info as possible. A sample csv export will be incredibly valuable to help speed up
development. During development, you may be contacted to help with alpha builds.

### Pull requests, licensing, usage, etc.
* This tool is not to be used in a commercial capacity, either for customer
support or for the distribution of tools
* This tool is available open-source, free for use in any nonprofit context.
* **PULL REQUESTS**: Please discuss your intent as soon as possible when creating a
pull request with the project owner(s).
* **FORKS**: Forks are welcome, so long as they are also used in a nonprofit context.
