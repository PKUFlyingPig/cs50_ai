import csv
import itertools
import os
import re
import sys


def main():
    if len(sys.argv) != 3:
        sys.exit("python construct.py data corpus")
    examples, corpus = load(sys.argv[1], sys.argv[2])
    templates = find_templates(examples, corpus)
    templates = filter_templates(templates, 2)
    results = extract_from_templates(templates, corpus)
    for result in results:
        print(result)


def load(data, directory):
    with open(data) as f:
        examples = list(csv.reader(f))
    corpus = ""
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename)) as f:
            corpus += f.read().replace("\n", " ")
    return examples, corpus


def find_templates(examples, corpus):
    templates = []
    for a, b in examples:
        templates.extend(match_query(a, b, True, corpus))
        templates.extend(match_query(b, a, False, corpus))

    # Find common middles
    middles = dict()
    for template in templates:
        middle = template["middle"]
        order = template["order"]
        if (middle, order) in middles:
            middles[middle, order].append(template)
        else:
            middles[middle, order] = [template]

    # Filter middles to only those used multiple times
    middles = {
        middle: middles[middle]
        for middle in middles
        if len(middles[middle]) > 1
    }

    # Look for common prefixes and suffixes
    results = []
    for middle in middles:
        found = set()
        for t1, t2 in itertools.combinations(middles[middle], 2):
            prefix = common_suffix(t1["prefix"], t2["prefix"])
            suffix = common_prefix(t1["suffix"], t2["suffix"])
            if (prefix, suffix) not in found:
                if (not len(prefix) or not len(suffix)
                   or not prefix.strip() or not suffix.strip()):
                        continue
                found.add((prefix, suffix))
                results.append({
                    "order": middle[1],
                    "prefix": prefix,
                    "middle": middle[0],
                    "suffix": suffix
                })
    return results


def filter_templates(templates, n):
    return sorted(
        templates,
        key=lambda t: len(t["prefix"]) + len(t["suffix"]),
        reverse=True
    )[:n]


def extract_from_templates(templates, corpus):
    results = set()
    for template in templates:
        results.update(match_template(template, corpus))
    return results


def match_query(q1, q2, order, corpus):
    q1 = re.escape(q1)
    q2 = re.escape(q2)
    regex = f"(.{{0,10}}){q1}((?:(?!{q1}).)*?){q2}(.{{0,10}})"
    results = re.findall(regex, corpus)
    return [
        {
            "order": order,
            "prefix": result[0],
            "middle": result[1],
            "suffix": result[2]
        }
        for result in results
    ]


def match_template(template, corpus):
    prefix = re.escape(template["prefix"])
    middle = re.escape(template["middle"])
    suffix = re.escape(template["suffix"])
    regex = f"{prefix}((?:(?!{prefix}).){{0,40}}?){middle}(.{{0,40}}?){suffix}"
    results = re.findall(regex, corpus)
    if template["order"]:
        return results
    else:
        return [(b, a) for (a, b) in results]


def common_prefix(*s):
    # https://rosettacode.org/wiki/Longest_common_prefix#Python
    return "".join(
        ch[0] for ch in itertools.takewhile(
            lambda x: min(x) == max(x), zip(*s)
        )
    )


def common_suffix(*s):
    s = [x[::-1] for x in list(s)]
    return common_prefix(*s)[::-1]


if __name__ == "__main__":
    main()
