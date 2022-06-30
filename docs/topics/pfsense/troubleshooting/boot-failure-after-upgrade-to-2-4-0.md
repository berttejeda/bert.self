---
title: 'Boot failure after upgrading pfsense to 2.4.0'
categories:
  - pfSense
tags:
  - router
  - firewall
  - networking
  - pfSense
---

### Scenario

You upgraded from pfsense 2.3x to 2.4.0 Upon reboot, I was unable to ssh to the box. Once at the physical console, I noticed pfsense had encountered a panic condition, barking about not being able to mount 

`/dev/ad0s1a` 

### Troubleshooting 

At the prompt, I typed in "?" to review the available block devices (disks and the like) 

I saw in the output the device `/dev/ada0s1a`, a slightly different device path from what the error message referred to.

I then entered in: `ufs:/dev/ada0s1a`, and boom, pfsense kicked off its regular routines (although it did keep barking about this or that package needing to be cleaned and such).

The permanent fix was to correct the mount references in /etc/fstab. 

I changed any reference to `ad0` to `ada0`, rebooted, and voila. 

Next time I upgrade pfsense, I'll read up on any known issues and the like. 

Hint Hint: 2.4 New Features and Changes: <https://doc.pfsense.org/index.php/2.4_New_Features_and_Changes#Known_Issues>