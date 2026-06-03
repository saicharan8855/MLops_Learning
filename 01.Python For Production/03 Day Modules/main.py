from iris_package.data import get_sample_data , split_data 
from iris_package.model import predict

def main() -> None:
    data = get_sample_data()
    print(f"length of data is {len(data)}")

    train , test = split_data(data , split = 0.8)
    print(f"length of train data is {len(train)}")
    print(f"length of test data is {len(test)}")

    for sample in test:
        result = predict(sample)
        print(f"features: {sample} , prediction: {result}")

if __name__ == "__main__":
    main()
