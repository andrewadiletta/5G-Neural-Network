Machine Learning based Mobile Network

This ML application includes 3 elements.  In this zip archive both the gui for the simulator and a simulator which generates the training data for a tensorflow based DNN will be found.

Additionally, the tensorflow based model is also here which learns from the simulator data.

The idea is that the simulator generates "images" based on user supplied obstacles and projected population density of mobile "hop" capable devices.  The simulator then generates thousands of possible scenarios, which are provided to the dnn.

The dnn learns best path.  This is then fed back into the simulator to see how well the DNN has performed when new random data is provided into that environment.  If you don't like the results you need to generate additional synthetic data to train the DNN further.

In deployment, the mobile user, upon finding their 5G connection is losing strength initiates an ad-hoc path to nearest known 5G access point.  However, given the learning - when the device requiring help calls out, only the devices known to gain access to the known 5G thru a known path respond...   Effectively, with source routing - the source says I know where I am, I know where I want to go, and the ML data says if someone in area X1 is available, please respond.   If not, someone in area X2 please respond...  and so on...

This project includes these dependencies:

python3
pygame
Numpy
tensorflow
tflearn

NOTE: This project only works on with python3. To Run, install the dependencies then run:

python3 main.py


The GUI will show the map on the left, some statistics on the bottom, and some buttons to experiment with on the right. You can increase and decrease the node count with the top two buttons. If the node count is small enough, the draw full mesh will enable, and you will be able to draw a full mesh connecting all the nodes.

The Batman mesh and dijkatras algorithm are other ways of connecting the nodes. There isn't a need to train the neural network, as the network is pretrained. 

The Blank Skynet Algorithm button will run on an untrained neural network. Slim skynet algorithm will run on a lightly trained neural network, and basic skynet algorithm will run on a more heavily trained network. 

Ideally, you will see a difference between blank and basic skynet algorithms, which will show that the neural network effectively mapped the 5G network. 

Shuffle changes the locations of the points. 

You can see a demonstation of the code here: https://www.youtube.com/watch?v=hqFHVZR4Gjk&t=105s



