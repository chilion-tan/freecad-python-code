# freecad-python-code: Code examples for Freecad Application
Example 1: TransferTinesToPalletTesting for animating / Simulating Pick & Place of Parts into container/cavities (Pallet).
Link to the video: https://drive.google.com/file/d/1JWBeLoY3x2t2Loo9MBT39WwwB5l0vkc1/view?usp=sharing
The code was developed to showcase two automated pick & place processes where 
1) Process 1: Parts (round disc in green) are conveyed to left and right side of a 48-cavities pallet. Two sets of XYZ sliders each with single part gripper will pick up parts and place them into cavities of the pallet. The filled pallet will be rotated to another location for process 2.
2) Process 2: Another robotic arm with 6-grippers end effector will pick 6 parts in one action and place them onto another
   sub-assembly

Example 2: MoveRotateClaw for animating / simulating opening and closing of 3 claws to pick a round object. The gripping action is controlled by sliding a threaded bar that has a linear cam mounted to it. 
Link to the video: https://drive.google.com/file/d/1734sql54cojLAIbOdflTz8fSLrHenqml/view?usp=sharing
The code was developed to showcase a mechanism used to pick parts using gripper. 
1) Video show only 2 claws to reduce computation in Freecad.
2) Threaded rod with cam move up & down by a air cylinder which will push and cause the gripging claws to rotate about their fulcrums.
3) The end of the threaded rod is designed to push off the round part fromthe claws
