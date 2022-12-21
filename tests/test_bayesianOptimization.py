
import numpy as np
from icecream import ic


from agroml.data import Data, ModelData
from agroml.cashOptimization import BayesianOptimization


rawdata = Data("tests/testData/dataExample.csv")
modelData = ModelData(
    data = rawdata,
    inputList = ["tx", "tn", "rs"],
    outputList = ["et0"])
modelData.splitToTrainTest(splitFunction="SplitRandom", testSize=0.3)
modelData.normalizeData(method= "StandardScaler")

def test_initialization():
    global modelData

    bayesianOptimization = BayesianOptimization(modelData)

    assert bayesianOptimization.modelData == modelData
    assert bayesianOptimization.splitFunction == "None"
    assert bayesianOptimization.validationSize == 0.2
    assert bayesianOptimization.randomSeed == 42
    assert bayesianOptimization.nFolds == 5
    assert bayesianOptimization.xVal is None
    assert bayesianOptimization.yVal is None

def test_splitToValidationUsingRandom():
    global modelData

    bayesianOptimization = BayesianOptimization(
        modelData = modelData,
        splitFunction = "SplitRandom",
        validationSize = 0.3,
        )
    
    assertDimensionsTrainAndVal(bayesianOptimization)
    assertLengthTrainAndVal(bayesianOptimization, modelData)
    assertTrainAndValIndexAreNotMonotonicallyIncreasingIndex(bayesianOptimization)

def test_splitToValidationUsingSequential():
    global modelData

    bayesianOptimization = BayesianOptimization(
        modelData = modelData,
        splitFunction = "SplitSequential",
        validationSize = 0.3,
        )

    assertDimensionsTrainAndVal(bayesianOptimization)
    assertLengthTrainAndVal(bayesianOptimization, modelData)
    assertTrainAndValIndexAreMonotonicallyIncreasingIndex(bayesianOptimization)

def assertDimensionsTrainAndVal(bayesianOptimization: BayesianOptimization):
    assert len(bayesianOptimization.xTrain.shape) == 3
    assert len(bayesianOptimization.xVal.shape) == 3
    assert len(bayesianOptimization.yTrain.shape) == 3
    assert len(bayesianOptimization.yVal.shape) == 3

def assertLengthTrainAndVal(bayesianOptimization: BayesianOptimization, modelData: ModelData):
    assert bayesianOptimization.xTrain.shape[1] == modelData.xTrain.shape[0] - bayesianOptimization.xVal.shape[1]
    assert modelData.xTrain.shape[0] == bayesianOptimization.xTrain.shape[1] + bayesianOptimization.xVal.shape[1]
    assert bayesianOptimization.yTrain.shape[1] == modelData.yTrain.shape[0] - bayesianOptimization.yVal.shape[1]
    assert modelData.yTrain.shape[0] == bayesianOptimization.yTrain.shape[1] + bayesianOptimization.yVal.shape[1]
    

def assertTrainAndValIndexAreMonotonicallyIncreasingIndex(bayesianOptimization: BayesianOptimization):
    assert bayesianOptimization.xTrainIndex.is_monotonic_increasing
    assert bayesianOptimization.xValIndex.is_monotonic_increasing
    assert bayesianOptimization.yTrainIndex.is_monotonic_increasing
    assert bayesianOptimization.yValIndex.is_monotonic_increasing

def assertTrainAndValIndexAreNotMonotonicallyIncreasingIndex(bayesianOptimization: BayesianOptimization):
    assert not(bayesianOptimization.xTrainIndex.is_monotonic_increasing)
    assert not(bayesianOptimization.xValIndex.is_monotonic_increasing)
    assert not(bayesianOptimization.yTrainIndex.is_monotonic_increasing)
    assert not(bayesianOptimization.yValIndex.is_monotonic_increasing)

def test_splitToValidationUsingKFold():
    global modelData

    bayesianOptimization = BayesianOptimization(
        modelData = modelData,
        splitFunction = "CrossValidation",
        nFolds = 5,
        )

    
    assertDimensionsTrainAndVal(bayesianOptimization)

    # not evaluated on purpose
    # We can lose some data due to Kfold (1 value as maximum per fold)
    #assertLengthTrainAndVal(bayesianOptimization, modelData)

    assert bayesianOptimization.xTrain.shape[0] == 5
    assert bayesianOptimization.xVal.shape[0] == 5
    assert bayesianOptimization.yTrain.shape[0] == 5
    assert bayesianOptimization.yVal.shape[0] == 5
    

