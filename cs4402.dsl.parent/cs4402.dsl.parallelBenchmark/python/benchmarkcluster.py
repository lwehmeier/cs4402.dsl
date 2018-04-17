import timeit
import os
from subprocess import call
import subprocess
from dask.distributed import Client
import json

cmdBase = ["java", "-Xmx8G", "-jar", "../../cs4402.dsl.solver/build/libs/cs4402.dsl.solver-V1.1-all.jar", "--json"]
cmdAlgorithm = {
    "FC":["--algorithm", "fc"],
    "MAC2.5":["--algorithm", "mac25"],
    "MAC3":["--algorithm", "mac3"]
#    "MAC3.1":["--algorithm", "mac31"]
    }
cmdVarHeuristic = {
    "Brelaz":["--var-heuristic", "brelaz"],
    "Domain":["--var-heuristic", "domain-size"],
    "DomDeg":["--var-heuristic", "dom-deg"],
#    "File":["--var-heuristic", "file-static"],
    "VarId":["--var-heuristic", "var-id"],
    "Width":["--var-heuristic", "min-width"],
    "Deg":["--var-heuristic", "degree"],
    "Card":["--var-heuristic", "cardinality"]
    }
cmdValHeuristic = {
    "Magnitude":["--val-heuristic", "magnitude-asc"],
    "Magnitude":["--val-heuristic", "magnitude-desc"],
    "MinConflict":["--val-heuristic", "min-conflict"],
    "Cruciality":["--val-heuristic", "cruciality"],
    "Promise":["--val-heuristic", "promise"]
    }
ITERATIONS = 75
CLUSTER = True
SCHEDULER="pc2-082-l:8786"
if CLUSTER:
    daskClient = Client(SCHEDULER)

def doExec(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = proc.stdout.read()
    output=output.decode()
    print(cmd)
    print(output)
    return json.loads(output)

def runIteration(iteration):
    os.chdir("/cs/home/lw96/IdeaProjects/cs4402.dsl/cs4402.dsl.parent/cs4402.dsl.parallelBenchmark/python")
    print("runIteration: " + str(iteration))
    files = os.listdir('benchmarkSet')
    files = [str(x) for x in files if x[0] != '.' and x[-4:] == ".csp"]
    res = {}
    for filename in files:
        res[filename] = runAllParamCombinations("benchmarkSet/"+filename)
    return res

def runAllParamCombinations(file):
    print("runAllParamCombinations: " + file)
    res = {}
    for alg in cmdAlgorithm.items():
        res[alg[0]]={}
        for varh in cmdVarHeuristic.items():
            res[alg[0]][varh[0]]={}
            for valh in cmdValHeuristic.items():
                try:
                    res[alg[0]][varh[0]][valh[0]] = doExec(cmdBase+alg[1]+varh[1]+valh[1]+["-F", file])
                except Exception as e:
                    pass
    return res


def runIterations():
    print("runIterations")
    if CLUSTER:
        l = daskClient.map(runIteration, range(ITERATIONS))
        results = daskClient.gather(l, "skip")
    else:
        results = []
        for iter in range(ITERATIONS):
            results.append(runIteration(iter))
    return results

def benchmarkSolver():
    ret = runIterations()
    with open("solverBenchmark_raw.pydata","w") as f:
        f.write(str(ret))
    with open("solverBenchmark.pydata","w") as f:
        f.write(json.dumps(ret))


if __name__=='__main__':
    benchmarkSolver()
