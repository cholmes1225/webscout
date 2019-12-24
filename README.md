# webscout

This is a web-based scouting app designed and used by FRC Team 1073, the Force Team.

This scouting app uses a Raspberry Pi as the web-server, connected via ethernet to 6 scouting tablets.

The scouting hardware layout consists of:

- 1 Raspberry Pi Model 3
- 1 8-port switch
- 6 Samsung Galaxy Tablets
- 7 Ethernet cables
- 6 micro-USB-to-Ethernet adapters
- 1 12V-to-120V inverter
- 1 robot battery

The scouting tablets are connected to the ethernet adapters, which allows them to be connected to the 8-port switch. The Raspberry Pi is also connected to the switch. The Raspberry Pi is powered on, and then the tablets are powered up.

This software is installed on the Raspberry Pi running Ubuntu 18.04 with apache2. The Raspberry Pi is configured with a static IP address (10.73.10.73). A web browser is launched on each scouting tablet, and this IP address is entered as the URL.

This software provides the ability to scout individual robots in an FRC match, gather the data into CSV files which can be imported into Excel or Tableau, and calculate an Offensive Performance Rating (OPR) for each robot and sort them into a simple "pick list".

This software currently scouts the 2019 Destination Deep Space FRC challenge.
