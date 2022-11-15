import click
import subprocess
import tempfile
import platform
import zipfile

LIMBOOLE={
    "Windows": "limboole.exe",
    "Darwin": "limbooleOSX",
    "Linux": "limboole-linux-amd64.exe"}.get(platform.system(), "limboole")

def run_limboole(limboole, formula):
    with tempfile.NamedTemporaryFile("r") as out, tempfile.NamedTemporaryFile("w") as inp:
        inp.write(formula)
        inp.flush()
        subprocess.check_call(f"{limboole} -s -o {out.name} {inp.name}", shell=True)
        limoutput = out.read()
    lines = limoutput.splitlines()
    result = {}
    if "% SATISFIABLE" in lines[0]:
        for line in lines[1:]:
            key, value = line.split("=", 1)
            result[key.strip()] = int(value.strip())
        return result
    else:
        raise ValueError("No solution")


def variables_bases(size):
    assert size % 2 == 0 and size >= 4 # only even size over 3 supported
    number = size * size
    width = len(str(number))
    vars = [f"v{i:0{width}d}" for i in range(number)]
    return vars

def fields(size):
    vars = variables_bases(size)
    while vars:
        row, vars = vars[:size], vars[size:]
        yield row

def variables_real(size):
    bases = variables_bases(size)
    width = len(str(size))
    vars = {}
    for v in bases:
        l = [None, ]
        for i in range(1, size + 1):
            l.append(f"{v}{i:0{width}d}")
        vars[v] = l
    return vars

@click.command()
@click.option("--size", "-s", type=int, default=4)
@click.option("--limboole", default=LIMBOOLE)
@click.argument("studentno")
@click.argument("assignments", nargs=-1)
def main(size, limboole, studentno, assignments):
    selector = studentno[-2:]
    if assignments:
        vars = {}
        for a in assignments:
            # the error checking is rough. This is a student assignment. Shrugh.
            assert "=" in a
            k, v = a.split("=")
            v = int(v)
            assert 1 <= v <= size, "the value assigned are constrained by the size of the sudoku"
            assert k in variables_bases(size)
            vars[k] = v
        print(vars)

        real = variables_real(size)
        print([real[k][v]for k, v in vars.items()])

    else:
        print(f"Sudoku Field of size {size}:")
        print("-----------------------------")
        print("")
        for row in fields(size):
            print(" ".join(row))
        print("")
        print("base variable names used for assignments in this program.")
    return
    with zipfile.ZipFile(formulas, "r") as zf:
        formula = zf.read(f"formulas/{selector}.limboole").decode("ascii")
    print(formula)
    results = []
    while True:
        try:
            part = [formula]
            part.extend(format_filter_result(i) for i in results)
            form = " & ".join(part)
            results.append(run_limboole(limboole, form))
            print(results[-1])
        except ValueError:
            break
    fn = f"solutions_{studentno}.txt"
    with open(fn, "w") as fp:
        fp.write(solutions(studentno, studentname, results))
    

if __name__ == "__main__":
    #print(repr(run_limboole("./limboole-linux-amd64.exe", "a&!b")))
    main()