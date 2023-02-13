# artificial_bots


## Table of Contents

1. [How To Run The Code](https://github.com/ilesha-sawarkar/artificial_bots/blob/kinematic_snake/README.md#1--how-to-run-the-code) 

2. [Details About The Code](https://github.com/ilesha-sawarkar/artificial_bots/blob/kinematic_snake/README.md#2-details-about-the-code)
3. [Random Shapes Generated](https://github.com/ilesha-sawarkar/artificial_bots/blob/kinematic_snake/README.md#3-random-shapes-generated)
4. [Fitness Function](https://github.com/ilesha-sawarkar/artificial_bots/blob/kinematic_snake/README.md#4-fitness-function)
5. [Citations](https://github.com/ilesha-sawarkar/artificial_bots/blob/kinematic_snake/README.md#5-citations-for-refernces-to-build-similar-projects)

---------------------------------------------------------------------------------------------------------------------------------------------------------

## 1.  How To Run The Code 

   To run the code just run the program search.py after cloning the repository to your local machine.


   Another option is to run the code "python3 search.py" from the terminal or command line window. Run this command after using cd and runnning this command from the directory where you have stored your cloned repository on your local machine.
   


## 2. Details About The Code

  * The code generate random morphologies by linking them using joints.
  * It starts with the function Create_Body() where a random number of links is decided for the morphology.
  * Following which a list of randomly placed 0's and 1's are generated that depict the sensor values of the morphology.
  * Using this information we visually seperate the **links with sensors** as *Green* and the **links without sensors** as *Blue*.
  * **Additionally:**
    * I have also added a *randomization of shapes and dimensions* at each link.
    * So a shape of cube and sphere is randomly decided by the random function at each link following which the joints and sensors are added.
    * The dimensions of each shape is also randomly decided at each link.
   
  * In the Create_Brain()
     * The list of sensors and motors are used to generate synapses and adjust the weights of each neuron.
     * Sensor and motor neurons are named as per the naming pattern followed in the function Create_Body().


## 3. Random Shapes Generated

  * The generated morphologies has three types of shapes:
     * Cube
     * Cuboid - *Elongated Cube*
     * Sphere
  * These morphologies are generated by random dimensions for the length, width and height.

## 4. Fitness Function
   * The fitness function at each generation is updating the parent's fitness by check the best fitness value for each of its child. The best fitness value of the child is taken as a new parent to generate more children at the the next generation.

## 5. Citations for Refernces to build similar projects
   *  [LudoBots](https://www.reddit.com/r/ludobots/wiki/installation/)
   *  [Pyrosim](https://github.com/jbongard/pyrosim)
