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

def format_filter_result(res):
    out = []
    for n, v in sorted(res.items()):
        if v:
            out.append(f"!{n}")
        else:
            out.append(n)
    return f"({' | '.join(out)})"

def solutions(no, name, solutions):
    output = []
    out = output.append
    out(f"name: {name}")
    out(f"student number: {no}")
    out(f"number of solutions: {len(solutions)}")
    out("solutions:")
    for sol in solutions:
        out(format_filter_result(sol))
    out("") # at least Unix text file should end with NL
    return "\n".join(output)

@click.command()
@click.option("--formulas", "-f", type=click.File(mode="rb"), default="./formulas.zip")
@click.option("--limboole", default=LIMBOOLE)
@click.argument("studentno")
@click.argument("studentname")
def main(formulas, limboole, studentno, studentname):
    selector = studentno[-2:]
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