# Notes regarding Florence



#Custom painting functions
I added the wipe and unwipe functions to the GUI_Paint.cpp file and then made sure the signatures of the new functions were also added to GUI_Paint.h.  Both functions were written by AI.  I had to go back and forth with it a bit explaining what worked and what didn't work until it got to a place I was reasonably happy.  I never defined the LCD driver type to it.  It would have done better if I had.  This was deliberately quick and dirty.  I just copied in at one point the contents of the GUI_Paint.cpp so it could see the methods available to it. 