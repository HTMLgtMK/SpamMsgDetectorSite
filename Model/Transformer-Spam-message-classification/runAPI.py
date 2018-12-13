from model_with_inference import inference
import argparse
import argparse
import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Transformer-attention')
    parser.add_argument('--msg', type=str, action= 'store', default='')
    args = parser.parse_args()
    
    inference_data = args.msg
    start_time = time.time()
    a=inference()
    # a(inference_data)
    predict = a.inferenceAPI(inference_data)
    print(predict) # <type 'numpy.int64'>
