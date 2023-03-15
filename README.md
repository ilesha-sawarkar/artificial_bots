# artificial_bots

## Inspiration
*Evolution is found in nature in **various different ways**. Some creatures evolve to have a **huge torso and small limbs some evolve to have fins.** Some genetic modification help creatures run faster. This sparked my curiosity to evolve the random generated morphologies to check how they behave when we change the way the joints.*


## Table of Contents

1. [Hypothesis](https://github.com/ilesha-sawarkar/artificial_bots/blob/3D-Creature_locomotion/README.md#1-hypothesis)
2. [Experiments Performed](https://github.com/ilesha-sawarkar/artificial_bots/blob/3D-Creature_locomotion/README.md#2-experiments-performed)
3. [Findings](https://github.com/ilesha-sawarkar/artificial_bots/blob/3D-Creature_locomotion/README.md#3-findings) 
4. [Graphs](https://github.com/ilesha-sawarkar/artificial_bots/blob/3D-Creature_locomotion/README.md#4-graphs-chart_with_upwards_trend)
5. [About The Code](https://github.com/ilesha-sawarkar/artificial_bots/blob/3D-Creature_locomotion/README.md#5-about-the-code)
6. [Random Shapes Generated](https://github.com/ilesha-sawarkar/artificial_bots/blob/3D-Creature_locomotion/README.md#6-random-shapes-generated)
7. [Generation of Body](https://github.com/ilesha-sawarkar/artificial_bots/blob/3D-Creature_locomotion/README.md#7-generation-of-body)
8. [Generation of Brain](https://github.com/ilesha-sawarkar/artificial_bots/blob/3D-Creature_locomotion/README.md#8-generation-of-brain)
9. [How Creatures are Evolved](https://github.com/ilesha-sawarkar/artificial_bots/blob/3D-Creature_locomotion/README.md#9-how-the-creatures-are-evolved)
10. [Animation of 3D Creature](https://github.com/ilesha-sawarkar/artificial_bots/blob/3D-Creature_locomotion/README.md#10-animation-of-3d-creature)
11. [2-Minute Video](https://github.com/ilesha-sawarkar/artificial_bots/blob/3D-Creature_locomotion/README.md#11-2-minute-video)
12. [How To Run The Code](https://github.com/ilesha-sawarkar/artificial_bots/blob/3D-Creature_locomotion/README.md#12-how-to-run-the-code)
13. [Fitness Function](https://github.com/ilesha-sawarkar/artificial_bots/blob/kinematic_snake/README.md#13-fitness-function)
14. [Citations](https://github.com/ilesha-sawarkar/artificial_bots/blob/3D-Creature_locomotion/README.md#14-references-used-to-build-this-project)

---------------------------------------------------------------------------------------------------------------------------------------------------------


## 1. Hypothesis
:pushpin: **"Do *Prismatic Joints* enable *Faster* :running: movement than the Revolute joints"** :pushpin:

## 2. Experiments Performed
   1) Control
      * The control creature had revolute joints specified as joint types
      * The creature was evolved to 200 generations with a populationSize of 10 with 5 randomSeeds at each iteration.
      * The Control Creature was built with a randomization of shapes and shape dimension lengths.
      * Moreover at each generation the Mutate function had a randomized option of either appending a link to the creatures, deleting a link or to not make any changes.
      
   2) Experimental
      * The experimental was similar to control except that the joints that were added in positive and negative direction of the creature in the x and y axises had a **prismatic joint type**.

## 3. Findings
   * From the experiments performed we can see that ________ joint has better capapbilities. It can enable the body to move better and faster than compare to ---------. This is possible because of the -------- movement of the joint.

## 4. Graphs :chart_with_upwards_trend:


## 5. About The Code
   ### Body
 * Initially a matrix is created to find all possible empty spaces in the 3d morphospace.
 * * If there is space in the world a cube, sphere or cuboid is added.
 * Accordingly the height, width, length is calculated with respect to each dimension and cuboidal space.
 * Pictographical representation of links and joints
 * The code generate random morphologies by linking them using joints.
 * It starts with the function Create_Body() where a random number of links is decided for the morphology.
 * Following which a list of randomly placed 0's and 1's are generated that depict the sensor values of the morphology.
 * Using this information we visually seperate the **links with sensors** as *Green* and the **links without sensors** as *Blue*.
 * **Additionally:**
   * I have added a *randomization of dimensions* at each link.
   * I have added a *randomization of shapes* at each link.
   * I have added a *randomization of the direction* at which a link will be appending to the main initial link to create 3D creatures.

  ### Brain

  * In the Create_Brain()
     * The list of sensors and motors are used to generate synapses and adjust the weights of each neuron.
     * Sensor and motor neurons are named as per the naming pattern followed in the function Create_Body().

  
## 6. Random Shapes Generated

  * The generated morphologies are made of three types of shapes:
     * Cube
     * Cuboid - *Elongated Cube*
     * Sphere
    
  * These morphologies are generated by random dimensions for the length, width and height.
 

## 7. Generation of Body
   * Initially a matrix is created to find all possible empty spaces in the 3d morphospace.
   * If there is space in the world a cube or cuboid is added. 
   * Accordingly the height, width, length is calculated with respect to each dimension and cuboidal space.
   * Pictographical representation of links and joints
   <img width="789" alt="Screenshot 2023-02-20 at 11 06 59 PM" src="https://user-images.githubusercontent.com/114837040/220252820-6dd4acd9-4b14-4f60-a826-e7f6d3a6f101.png">

    
   * Below is the 3D Creature generated by the above positioning of cubes:


     <img width="441" alt="Screenshot 2023-02-20 at 11 06 08 PM" src="https://user-images.githubusercontent.com/114837040/220252645-7671ce8b-e035-4910-9cc3-e97b2810a3dc.png">
     
     

## 8. Generation of Brain
   * For the Generation of Brain first we calculate the total number of sensors in the data by counting the 1's.
   * We already have a count of the motor Neurons by simpling appending the name of the joint Link after creation to the motor Neuron list.
   * After which we send a sensor neuron to each joint created.
   * We can then iterate and adjust the weights which are used to Send the synapse(movement) to the joints
   * Below is the flowchart depicting the generation of brains.

  <img width="757" alt="Screenshot 2023-03-14 at 10 09 50 PM" src="https://user-images.githubusercontent.com/114837040/225196003-8047518f-f15d-49c5-beb8-e631d55bd0d7.png">

## 9. How the Creatures are Evolved

  ### 1) Evolution of Body
  * At each generation the creatures are evolved as per the random mutation selected.
  * The random choice is done to append, delete or to let the creature remain as it is.
  
    #### Appending a link to the Creature
    * After this a randomization of dimension and link shape is done following which we proceed to check whether the links can be added to the matrix.
    * If so then they are added to the body of the creature by checking whether the maximum and minimum of each coordinates do not coincide with any other shapes.
    * And additional check is added so that the links are not more than the maximum number of links. *This check was added since pybullet sometimes may crash halfway in the simulation due to insufficient memory.*

    #### Deleting Links from the Creature
    * A link is randomly chosen for deletion from the creature based on whether the creature is able to move fast or not.
    * A constraint is added so that a link is not deleted whose subchildren are present in the urdf.
    * If the link has children than another link is chosen randomly to prevent errors since joints have a hierachy.


 <img width="647" alt="Screenshot 2023-03-14 at 10 33 48 PM" src="https://user-images.githubusercontent.com/114837040/225199596-808cbe78-d5d0-4c0e-845f-e21c67772a20.png">
 

  ### 2) Evolution of Brain
  * At each generation the creatures are evolved as per the random mutation selected.
  * The random choice is done to append, delete or to let the creature remain as it is.
  
    #### Appending a link to the Creature
    * After this a randomization of dimension and link shape is done following which we proceed to check whether the links can be added to the matrix.
    * If so then they are added to the body of the creature by checking whether the maximum and minimum of each coordinates do not coincide with any other shapes.
    * And additional check is added so that the links are not more than the maximum number of links. *This check was added since pybullet sometimes may crash halfway in the simulation due to insufficient memory.*

    #### Deleting Links from the Creature
    * A link is randomly chosen for deletion from the creature based on whether the creature is able to move fast or not.
    * A constraint is added so that a link is not deleted whose subchildren are present in the urdf.
    * If the link has children than another link is chosen randomly to prevent errors since joints have a hierachy.
    * 


## 10. Animation of 3D Creature
   * [Youtube Link](https://youtu.be/l4iixwTlNHU)
   
   
   * Example of the 3D Creature generated
   
   <img width="814" alt="Screenshot 2023-02-20 at 10 16 27 PM" src="https://user-images.githubusercontent.com/114837040/220246470-70a84778-34e6-45b4-a17b-44154798a56f.png">
   
## 11. 2-Minute Video
   * [Youtube Link](https://youtu.be/l4iixwTlNHU)
## 13. How To Run The Code 

   To run the code just run the program search.py from any after cloning the repository to your local machine.


   Another option is to run the code "python3 search.py" from the terminal or command line window. Run this command after using cd and runnning this command from the directory :file_folder: where you have stored your cloned repository on your local machine.
  
  Fitness Function :chart_with_upwards_trend:
   * The fitness function at each generation is updating the parent's fitness by check the best fitness value for each of its child. The best fitness value of the child is taken as a new parent to generate more children at the the next generation.
   * The fitness function helps evolve the morphology to walk in x-coordinate direction by taking xPosition in the Get_Fitness() in the robot.py file.



## 14. References used to build this project
   *  [LudoBots](https://www.reddit.com/r/ludobots/wiki/installation/)
   *  [Pyrosim](https://github.com/jbongard/pyrosim)
