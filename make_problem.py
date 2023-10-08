import os
import sys
import yaml

# Meta data
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    # Get name
    name = input('Enter problem name: ').strip()
    dir_name = f'problem_{name}'

    # Make directory
    try:
        os.makedirs(dir_name)
    except OSError:
        print('Problem alread exists!', file=sys.stderr)
        exit(1)

    # Make gen.py
    with open(os.path.join(APP_ROOT, dir_name, 'gen.py'), 'w') as gen_py_file:
        with open(os.path.join(APP_ROOT, 'templates', 'gen.py.template'), 'r') as template:
            gen_py_file.write(template.read())

    problem_dir = os.path.join(APP_ROOT, 'problems', 'problems.yaml')
    
    # Add problem to problems.yaml
    with open(problem_dir, 'r') as problems_file:
        try:
            problems = yaml.safe_load(problems_file)
        except yaml.YAMLError:
            print('Invalid problem file format (Ensure YAML)', file=sys.stderr)

    problems['problems'][name] = {'testcases': 10}

    with open(problem_dir, 'w') as problems_file:
        try:
            yaml.safe_dump(problems, problems_file, default_flow_style=False)
        except yaml.YAMLError:
            print('Failed to write yaml to problems.yaml', file=sys.stderr)
