#! -*- coding: UTF-8 -*-
import shutil
import jinja2
import os
import subprocess
import glob


def get_var_index(params):
    template = os.path.join(params['directory'], 'template.ctl')
    ctl_template = open(template, 'r')
    text = ctl_template.read()
    ctl_template.close()
    vars = text.split('VARS')[1].split('\n')[1:-1]
    for i, v in enumerate(vars):
        vname = v.split()[0]
        if params['var_name'] in vname:
            params['ind_var'] = i
            break


def fill_template(params):
    base_dir = os.path.dirname(__file__)
    template_dir = os.path.join(base_dir, "templates")
    template_loader = jinja2.FileSystemLoader(searchpath=template_dir)
    template_env = jinja2.Environment(loader=template_loader)
    TEMPLATE_FILE = "extrair_template.tcl"
    template = template_env.get_template(TEMPLATE_FILE)
    output = template.render(params)
    output_file = open(params['output_tcl'], 'w')
    output_file.write(output)
    output_file.close()


def convert_to_nc(params):
    os.environ['PATH'] += os.pathsep + '/scratchin/prod/um/home/umrun/prj/xconv'
    to_conv = params['output_tcl']
    convsh_cmd = 'convsh ' + to_conv
    subprocess.call(convsh_cmd.split())
    

def run_script(params, cmp):
    ferret = '/scratchin/prod/mbscg/home/mbscg/software/ferret/bin/ferret'
    if cmp: #versao 3
        command = '{} -gif -nojnl -script {} {} {} {} {} {}'
    else:
        command = '{} -gif -nojnl -script {} {} {}'
    script = 'analise-automaticaV1.1.jnl'
    script_v2 = 'analise-automaticaV2.5.jnl'
    script_v3 = 'analise-automaticaV3.jnl'
    orig_nc = params['output_nc']
    variable = params['var_name']
    final_year = params['final_year']
    plot_area = params['plot_area']
    if cmp:
        command = command.format(ferret, script_v3, orig_nc, variable, cmp['output_nc'], variable, plot_area)
    else:
        command = command.format(ferret, script, orig_nc, variable)
    subprocess.call(command.split())


def gen_figs(params, cmp=None):
    for v in params['var_names']:
        try:
            params['var_name'] = v
            #params['output_nc'] = '-'.join([v, params['output_nc'])
            if cmp:
                cmp['var_name'] = v
                #cmp['output_nc'] = '-'.join([v, cmp['output_nc'])
            get_var_index(params)
            if cmp:
                get_var_index(cmp)
            fill_template(params)
            if cmp:
                fill_template(cmp)
            convert_to_nc(params)
            if cmp:
                convert_to_nc(cmp)
            run_script(params, cmp)
        except:
            print "skipping var", v
