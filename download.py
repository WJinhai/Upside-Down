import pickle
from subprocess import Popen, PIPE

filename = 'data/kkf.txt'

if __name__ == '__main__':
    with open(filename, 'r') as f:
        lines = f.readlines()

    samples = []
    for i, line in enumerate(lines[1:]):
        tokens = line.split('\t')
        publish_date = tokens[0]
        oss_filepath = tokens[1].strip()
        oss_image_url = tokens[3].strip()
        oss_image_url = oss_image_url.split(',')[0].strip()
        result = int(tokens[4])
        try:
            real = int(tokens[5])
        except ValueError:
            real = 0

        folder = 'data/kkf'
        process = Popen(["wget", '-N', oss_filepath, "-P", folder], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
        image_filename = oss_filepath[oss_filepath.rfind("/") + 1:]

        process = Popen(["wget", '-N', oss_image_url, "-P", folder], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
        xiaoyang_filename = oss_image_url[oss_image_url.rfind("/") + 1:]

        samples.append({'idx': i, 'image': image_filename, 'xiaoyang': xiaoyang_filename, 'result': result, 'real': real})

        with open('data.pkl', 'wb') as f:
            pickle.dump(samples, f)
