import yaml
import time
import os
import shutil
import stat
import glob
import gen_figs
import json


config = yaml.load(open('figures.config', 'r'))
permissions = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP |\
              stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH


 
def gen_figures():
    aqui = os.path.dirname(__file__)

    # run orders
    orders = glob.glob(os.path.join(aqui, '*order.json'))
    for _order in orders:
        order = json.load(open(_order, 'r'))
        print order

        var_names = order['variables'].split()
        var_groups = {'atmos': [], 'ocean': []}
        for var_spec in var_names:
            group, name = var_spec.split(':')
            var_groups[group].append(name)


        for realm in ['atmos', 'ocean']:
            params = {'output_tcl': '{}_{}.tcl'.format(order['exp'], order['member']),
                'output_nc': '{}-{}.nc'.format(order['exp'], order['member']), 
                'var_names': var_groups[realm],
                'exp': order['exp'],
                'final_year': order['final_year'],
                'member': order['member'],
                'realm': realm,
            }

            if order['plot_area']:
                params['plot_area'] = order['plot_area']
            else:
                params['plot_area'] = '80E 80E 90N 90S'

            # find directory
            template_directory = '/stornext/online*/ocean/simulations/{}/dataout/ic12/ic*/{}/{}/CGCM_MEAN'
            template_directory_alt = '/stornext/online*/ocean/simulations/{}/dataout/ic12/ic*/{}/{}/CGCM'

            directory = template_directory.format(params['exp'],params['member'],params['realm'])
            directory_alt = template_directory_alt.format(params['exp'],params['member'],params['realm'])
            possible = glob.glob(directory)
            possible_alt = glob.glob(directory_alt)

            if not possible and possible_alt:
                possible = possible_alt

            if possible:
                params['directory'] = possible[0]

            c_params = None
            cmp_possible = []
            if order.has_key('comp_to'):
                cmp_exp, cmp_member = order['comp_to'].split()
                c_params = {'output_tcl': '{}_{}.tcl'.format(cmp_exp, cmp_member),
                    'output_nc': '{}-{}.nc'.format(cmp_exp, cmp_member),
                    'var_names': var_groups[realm],
                    'exp': cmp_exp,
                    'final_year': order['final_year'],
                    'member': cmp_member,
                    'realm': realm,
                    
                }

                cmp_directory = template_directory.format(c_params['exp'], c_params['member'],c_params['realm'])
                cmp_directory_alt = template_directory_alt.format(c_params['exp'], c_params['member'],c_params['realm'])
                cmp_possible = glob.glob(cmp_directory)
                cmp_possible_alt = glob.glob(cmp_directory_alt)

                if not cmp_possible and cmp_possible_alt:
                    cmp_possible = cmp_possible_alt

                if cmp_possible:
                    c_params['directory'] = cmp_possible[0]

            if possible:
                if c_params and cmp_possible:
                    gen_figs.gen_figs(params, cmp=c_params)
                else:
                    gen_figs.gen_figs(params)

            # moving things
        figs = []
        for v in var_groups['atmos']:
            figs += glob.glob('*{}*'.format(v))
        for v in var_groups['ocean']:
            figs += glob.glob('*{}*'.format(v))
        destino = os.path.join(config['figs_destino'], '_'.join([params['exp'], params['member']]))
        if os.path.exists(destino):
            shutil.rmtree(destino)
            os.makedirs(destino)
            os.chmod(destino, permissions)
        for fig in figs:
            os.chmod(fig, permissions)
            shutil.move(fig, destino)

        # consumed, delete
        os.remove(_order)
        [os.remove(t) for t in glob.glob('*.nc')]
        [os.remove(t) for t in glob.glob('*.tcl')]


if __name__ == "__main__":
    print "generating figures"
    gen_figures()
