from typing import List , Tuple

def create_sample_data() -> List[List[float]]:
    
    return [
        [3.2 , 1.5 , 1.2 , 2.0],
        [2.8 , 3.4 , 5.2 , 1.0],
        [1.2 , 2.9 , 3.5 , 4.1],
        [5.2 , 5.6 , 3.2 , 5.9]
    ]

def split_data(data:List[List[float]] , split: float = 0.8) -> Tuple[List[List[float]] , List[List[float]]]:
    
    split_index = int((len(data) * split))
    return data[:split_index] , data[split_index:]