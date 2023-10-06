from typing import Tuple

import os
import sys
import yaml
import types
import shutil

import importlib.machinery
import importlib.util

from tqdm import tqdm


def load_module(module_file_path: str, module_name: str) -> types.ModuleType:
    loader = importlib.machinery.SourceFileLoader(
        module_name, module_file_path)
    spec = importlib.util.spec_from_loader(module_name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def generate_testcase_dirs(problem_dir: str, problem_name: str) -> Tuple[str, str]:
    testcases_dir_path = os.path.join(problem_dir, 'testcases')
    if not os.path.exists(testcases_dir_path):
        os.mkdir(testcases_dir_path)

    problem_path = os.path.join(
        testcases_dir_path, f'{problem_name}_testcases')
    if os.path.exists(problem_path):
        shutil.rmtree(problem_path)

    inputs_dir = os.path.join(problem_path, 'input')
    outputs_dir = os.path.join(problem_path, 'output')

    os.mkdir(problem_path)
    os.mkdir(inputs_dir)
    os.mkdir(outputs_dir)

    return inputs_dir, outputs_dir, problem_path


if __name__ == '__main__':
    gen_name = 'gen'
    gen_file_name = f'{gen_name}.py'
    problems_file_name = 'problems.yaml'

    root_dir = os.path.dirname(__file__)
    problems_path = os.path.join(root_dir, problems_file_name)

    if os.path.exists(problems_path):
        with open(problems_path, 'r') as problem_yaml_file:
            try:
                problems = yaml.safe_load(problem_yaml_file)['problems']
            except yaml.YAMLError:
                print('Invalid problem file format (Ensure YAML)',
                      file=sys.stderr)
    else:
        print(f'Cannot find problems file: `{problems_file_name}`',
              file=sys.stderr)

    for problem in problems:
        problem_name = problem['name']
        testcase_count = problem['testcases']
        problem_dir = os.path.join(root_dir, problem_name)
        if testcase_count <= 0:
            print(f'Ignoring problem: {problem_name}')
            continue
        if os.path.exists(problem_dir):
            problem_gen_path = os.path.join(problem_dir, gen_file_name)
            if os.path.exists(problem_gen_path):
                print(f'Generating testcases for problem: {problem_name}')

                inputs_dir, outputs_dir, problem_dir = generate_testcase_dirs(
                    problem_dir, problem_name)
                generator = load_module(problem_gen_path, gen_name)

                progress_bar_format: str = '{l_bar}{bar}| [{elapsed}<{remaining}, {n}/{total}, {rate_fmt}{postfix}]'
                testcases_bar = tqdm(range(testcase_count),
                                     bar_format=progress_bar_format, unit='tc')
                for i in testcases_bar:
                    input_s = generator.generate_inputs(i)
                    output_s = generator.solution(input_s)

                    index_s = str(i).zfill(2)
                    input_file_path = os.path.join(
                        inputs_dir, f'input{index_s}')
                    output_file_path = os.path.join(
                        outputs_dir, f'output{index_s}')

                    with open(input_file_path, 'w') as input_file:
                        input_file.write(input_s)
                    with open(output_file_path, 'w') as output_file:
                        output_file.write(output_s)

                    zip_path = f'{problem_dir}.zip'
                    if os.path.exists(zip_path):
                        os.remove(zip_path)
                    shutil.make_archive(problem_dir, 'zip', problem_dir)
            else:
                print(f'Cannot find `{gen_file_name}` in folder `{problem_dir}`',
                      file=sys.stderr)
        else:
            print(f'Cannot find problem folder: {problem_dir}',
                  file=sys.stderr)
