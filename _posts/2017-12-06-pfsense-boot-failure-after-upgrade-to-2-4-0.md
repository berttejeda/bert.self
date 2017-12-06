---
ID: 903
post_title: 'pfsense &#8211; Boot failure after upgrade to 2.4.0'
author: Bert Tejeda
post_excerpt: ""
layout: post
permalink: >
  http://bertdotself.com/pfsense-boot-failure-after-upgrade-to-2-4-0/
published: true
post_date: 2017-12-06 14:53:18
---
# Scenario Upgraded from pfsense 2.3x to 2.4.0 Upon reboot, I was unable to ssh to the box. Once at the physical console, I noticed pfsense had encountered a panic condition, barking about not being able to mount /dev/ad0s1a 

# Troubleshooting At the prompt, I typed in "?" to review the available block devices (disks and the like) I saw in the output the device 

`/dev/ada0s1a`, a slightly different device path from what the error message referred to. I then enter in: `ufs:/dev/ada0s1a`, and boom, pfsense kicked off its regular routines (although it did keep barking about this or that package needing to be cleaned and such) The permanent fix was to correct the mount references in /etc/fstab. I changed any reference to `ad0` to `ada0`, rebooted, and voila. Next time I upgrade pfsense, I'll read up on any known issues and the like. Hint Hint: 2.4 New Features and Changes: (https://doc.pfsense.org/index.php/2.4_New_Features_and_Changes#Known_Issues))[https://doc.pfsense.org/index.php/2.4_New_Features_and_Changes#Known_Issues]