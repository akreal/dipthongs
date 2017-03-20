#!/usr/bin/env python3

import glob
import subprocess
from scipy.optimize import minimize

def loss(x, debug=False):
    [wbeam, beam] = x
    results = []

    for wav in glob.glob('*.wav'):
        wav_word = wav[:-6]

        #for jsgf in glob.glob('*-dipthongs.jsgf'):
        for jsgf in glob.glob('*.jsgf'):
            jsgf_word = jsgf[:jsgf.rindex('-')]

            try:
                output = subprocess.check_output([
                    'pocketsphinx_continuous',
                        '-infile', wav,
                        '-jsgf', jsgf,
                        '-dict', 'phonemes.dict',
                        '-fsgusefiller', 'no',
                        '-bestpath', 'no',
                        '-wbeam', str(wbeam),
                        '-beam', str(beam)
                ], stderr=subprocess.DEVNULL, universal_newlines=True)
            except subprocess.CalledProcessError:
                output = ''

            if debug:
                print('{} - {} - "{}"'.format(wav, jsgf, output.strip()))

            if (wav_word == jsgf_word and output != '') or (wav_word != jsgf_word and output == ''):
                results.append(1)
            else:
                results.append(0)


    if len(results) > 0:
        result = float(sum(results)) / float(len(results))
    else:
        result = 0.0

    return 1 - result


wbeam = 1e-48
beam = 7e-29

res = minimize(
                loss,
                [wbeam, beam],
                method='Powell',
                jac=False,
                options={'disp': True}
)

print(res.x)

print(loss(res.x, True))
