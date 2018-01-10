# CAPVC
Cycle Animation Playblast and Version Control

Tool Created by Mendel Reis (mendelreis@gmail.com)

What is:
-Maya 2017 custom tool that organizes cycle animations and playblasts versions.

What does it do: 
-Lets you specify idle name, start and end frame, information about the cycle and the playblast version you last did. Playblast it nicelly for you

How to run it: 
-Just copy the load the file into your Maya script editor and run it. You can also drag it to your own shelf. 

Features: 
-choose which cycles to perform playblast, selected or all.
-saves file video file with naming convention: PREFIX_CYCLENAME_000_SUFFIX
-can save separated cycles into respective folder inside specified path 
-lets you choose format, codec and size.
-lets you pick the camera you want to playblast
-create new version or overwrite previous version
-output video with custom HUD at the bottom right corner: 
  --Cycle name
  --Info
  --Version
  --Date  (The date is displayed as YY/MM/DD)
  --Animator
  --CurrentFrame
-edit cycles name, start, end, information, and delete cycle.
-has a custom warning area that tells you common errors


Issues and annoyances:
-Somehow it freezes  maya (on my macOS) if you input non utf-8 charactes when adding a new cycle (ç, ´, `, ^, ~, etc. ) So, for now,DO NOT use those characters. In windows it won't work, but did at least did not freeze the software.
-Before playblasting, make sure you click on a viewport. it wont work if the last maya window you clicked was the script editor o the outliner. 
So far that's what I got. Will update if needed.  


"Under the hood":
-To save data this tool creates a node in your scene. It is a simple transform node called cycleAnimationListNode. You can't edit or delete this node normally. it is locked. If you need to remove this node from your scene, go to EDIT -> Remove Node. This will delete the node and close the tool window and, of course, you will loose all the information you had you your previous cycles. To restart (fresh) after this, just run the tool again. If you delete the node by accident, don't freak out, just use the undo command (CTRL+Z). the removal of the node is a simple script that unlocks the node and deletes it, so, undo works fine. 


Considerations:
-This is a script I wrote not only to improve my workflow as a freelancer animator, but also to learn how to code. So, It is possible that there are many mistakes in this tool and your feedback would be most appreciated.
The code is not yet commented. There are some notations that helped me not get lost, but i confess that is not a proper coding workflow and if you want to know about something there, just let me know and I'll get back to you asap.
Also, I kinda 'brute forced' this script as I learned many of the code functionality while coding it, therefore, I don't consider it a clean code nor the most economy or elegant, but it seems to be working. If you have any improvements to make or tips, I'd love to hear it. 
That is it! Thank you.
