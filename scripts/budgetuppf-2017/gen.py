import re

def main():
    # read sophias result

    with open("sophia.txt", "r") as f:
        res_in_lines = f.read().splitlines()

    current_1 = None
    current_2 = None
    current_3 = None
    res_lines = []

    for line in res_in_lines:
        line = line.strip()

        if "summa" in line.lower():
            pass
        elif "=" in line:
            current_3 = line.split("=")[0].strip()
            x = float(line.split("=")[1].replace("+", "").replace(" ", "").replace(",", ".").replace("−", "-"))
            res_lines.append([current_1, current_2, current_3, x])
        elif re.match("\w+\d+", line):
            current_2 = line
        elif line:
            current_1 = line
        else:
            pass

    # read budget

    with open("budget.csv", "r") as f:
        budget_in_lines = f.read().splitlines()

    current_1 = None
    current_2 = None
    current_3 = None
    budget_lines = []

    for line in budget_in_lines:
        line = line.strip()

        if not line:
            continue

        a, b = line.split(",")

        if not a:
            continue

        if "summa" in a.lower():
            continue

        if "mål" in a.lower():
            continue

        if not b:
            if re.match("\w+\d+", a):
                current_2 = a
            else:
                current_1 = a
        else:
            current_3 = a
            x = float(b)
            budget_lines.append([current_1, current_2, current_3, x])

    # generate report lines

    report_lines = []

    check = False

    for budget_line, res_line in zip(budget_lines, res_lines):
        if budget_line[:2] != res_line[:2]:
            print("mismatch error")
            print(budget_line)
            print(res_line)
            exit()

        if check:
            a = budget_line[2]
            b = res_line[2]
            if a != b:
                print("{:>30} {:>30}".format(a, b))

        report_lines.append(budget_line + [res_line[3]])

    if len(budget_lines) != len(res_lines):
        print("len mismatch error")
        exit()

    # generate report

    doc = []
    doc += pre

    tcum_b = tcum_r = tcum_d = 0.0

    cum_b = cum_r = cum_d = 0.0
    last_c1 = last_c2 = None

    for i, line in enumerate(report_lines):
        c1, c2, c3, b, r = line
        d = r - b

        if not last_c1 or c1 != last_c1:
            if last_c1:
                doc += sumlines(cum_b, cum_r, cum_d)
                doc += endtab

            doc += begintab
            doc += newc1(c1)
            cum_b = 0
            cum_r = 0
            cum_d = 0

        if not last_c2 or c2 != last_c2:
            doc += ["    \\textbf{%s} \\\\"%c2]

        doc += ["    %s & %s & %s & %s \\\\"%(c3, mfmt(b), mfmt(r), mfmt(d))]

        cum_b += b
        cum_r += r
        cum_d += d

        tcum_b += b
        tcum_r += r
        tcum_d += d

        last_c1 = c1
        last_c2 = c2

    doc += sumlines(cum_b, cum_r, cum_d)
    doc += endtab

    doc += begintab
    doc += newc1("Total summa")
    doc += sumline(tcum_b, tcum_r, tcum_d)
    doc += endtab

    doc += post

    with open("out.tex", "w") as f:
        f.write("\n".join(doc))

    print("done")

pre = [
    "\\documentclass[../_main/handlingar.tex]{subfiles}",
    "",
    "\\begin{document}",
    "",
    "\\subsection{Budgetuppföljning för 2017}",
]

post =  [
    "",
    "\\newpage",
    "",
    "\end{document}",
    ""
]

begintab = ["", "\\begin{tabularx}{12cm}{X r r r}"]
endtab = ["\\end{tabularx}"]

def mfmt(x):
    return "\\SI{%.0f}{kr}"%x

def newc1(s):
    return [
        "    \\textbf{\\large %s} & \\textbf{Budget} & \\textbf{Resultat} & \\textbf{Differans} \\\\"%s,
        "    \\hline"
    ]

def sumlines(b, r, d):
    return ["    \\hline"] + sumline(b, r, d)

def sumline(b, r, d):
    return ["    \\textbf{Summa} & \\textbf{%s} & \\textbf{%s} & \\textbf{%s} \\\\"%(mfmt(b), mfmt(r), mfmt(d))]

main()
