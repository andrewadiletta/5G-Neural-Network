Machine Learning based Mobile Network

This ML application includes 3 elements.  In this zip archive both the gui for the simulator and a simulator which generates the training data for a tensorflow based DNN will be found.

Additionally, the tensorflow based model is also here which learns from the simulator data.

The idea is that the simulator generates "images" based on user supplied obstacles and projected population density of mobile "hop" capable devices.  The simulator then generates thousands of possible scenarios, which are provided to the dnn.

The dnn learns best path.  This is then fed back into the simulator to see how well the DNN has performed when new random data is provided into that environment.  If you don't like the results you need to generate additional synthetic data to train the DNN further.

In deployment, the mobile user, upon finding their 5G connection is losing strength initiates an ad-hoc path to nearest known 5G access point.  However, given the learning - when the device requiring help calls out, only the devices known to gain access to the known 5G thru a known path respond...   Effectively, with source routing - the source says I know where I am, I know where I want to go, and the ML data says if someone in area X1 is available, please respond.   If not, someone in area X2 please respond...  and so on...

This project includes these dependencies:

python3
pygame
tensorflow
tflearn

After unzipping, please use main to initiate the GUI and the mesh tools.

good luck.

