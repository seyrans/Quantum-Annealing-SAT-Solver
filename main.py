import dwavebinarycsp
import dimod
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
from dwave.system import LeapHybridSampler


# res = next(resp.data(['sample', 'energy'])).sample
def print_samples(sample, energy, is_satisfiable):
  res = sample
  res = {k:v for k,v in res.items() if str(k).isdigit()}
  import collections
  res = collections.OrderedDict(sorted(res.items()))
  ans = [str(key) if int(val) > 0 else str(-1 * int(key)) for key, val in res.items() if str(key).isdigit()]
  print('Is Satisfiable?', is_satisfiable,' | Energy:', energy, "|" ," ".join(ans))

def strip_file_spaces(file_path):
  """
  This function removes spaces from the beginning of the each line of the input
  """
  with open(file_path, 'r') as file_: 
    lines = file_.readlines()
    for i in range(len(lines)):
      lines[i] = lines[i].strip()
  with open('./current_file.cnf', 'w') as file_:
    for line in lines:
      file_.write('%s\n' % line)


cnf_file_path = "./pysgen/allbenchmarks/sgen-base-s32-g4-2.cnf"
strip_file_spaces(cnf_file_path)
with open('./current_file.cnf', 'r') as file_: 
  csp = dwavebinarycsp.cnf.load_cnf(file_)
  print('# Variables', len(csp.variables), '- # Constraints', len(csp), )
  bqm = dwavebinarycsp.stitch(csp)
  for i in range(3):
    # response = dimod.ExactSolver().sample(bqm)

    # response = dimod.SimulatedAnnealingSampler().sample(bqm)

    # sampler = EmbeddingComposite(DWaveSampler())
    # response = sampler.sample(bqm, num_reads=10)

    # sampler = LeapHybridSampler()         
    # response = sampler.sample(bqm)

    for sample, energy in response.data(['sample', 'energy']):
        is_satisfiable = csp.check(sample)
        if not is_satisfiable: continue
        print_samples(sample, energy, is_satisfiable)
