import csv

test = [{'loss': 50.17863674982058, 'status': 'ok', 'param': -7.0836880754181}, {'loss': 4.8042231382790055, 'status': 'ok', 'param': -2.1918538131634158}, {'loss': 41.01759999959909, 'status': 'ok', 'param': -6.40449841904884}, {'loss': 0.23830689431566277, 'status': 'ok', 'param': -0.48816687138279136}, {'loss': 7.583621674175589, 'status': 'ok', 'param': -2.753837626690359}]

def __write_to_csv(result_list):
    with open('crypto_bot/optimize/results.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for item in result_list:
            #output = str(key + " "+ str(text_dict[key])) 
            writer.writerow(str(item))
            
__write_to_csv(test)