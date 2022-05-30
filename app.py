from numpy import size
from modules import *
import gui


def main():
    ann = neural_network.NeuralNetwork()
    initialization = gui.GUI(ann)
    
    

    #table view
    #data = DataLoader.Data()

    #test = TrainAndTest.TrainAndTest()

    

    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #     print(data.movies.head())
    pass


if __name__ == "__main__":
    main()

