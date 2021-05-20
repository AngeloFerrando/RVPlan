import os
import sys
import time
import json

def parameterisedMonitor(domain_file_name):
    domain = open(domain_file_name, 'r')
    domain_text = domain.read()
    domain.close()
    fo_ltl_list = []
    start = 0
    while True:
        act = domain_text.find(':action', start)
        par = domain_text.find(':parameters', start)
        pre = domain_text.find(':precondition', start)
        eff = domain_text.find(':effect', start)
        if act == -1 or par == -1 or pre == -1 or eff == -1:
            break
        next_act = domain_text.find(':action', par)
        action, parameters_list, precondition_list, effect_list = extract_info(domain_text, act, par, pre, eff, next_act)
        # dynamic_pred = set()
        # for e in effect_list:
        #     if not e.startswith('!'):
        #         dynamic_pred.add(e[:e.find('(')])
        fo_ltl = ''
        for p in parameters_list:
            fo_ltl = fo_ltl + 'Forall ' + p.replace('?', '') + ' . '
        fo_ltl = fo_ltl
        fo_ltl = fo_ltl + action + '('
        for p_i in range(0, len(parameters_list)):
            if p_i != 0: fo_ltl = fo_ltl + ', '
            fo_ltl = fo_ltl + parameters_list[p_i].replace('?', '')
        fo_ltl = fo_ltl + ') -> '
        for p_i in range(0, len(precondition_list)):
            if p_i != 0: fo_ltl = fo_ltl + ' & '
            index = precondition_list[p_i].find('?', 0)
            vars = []
            while index != -1:
                index1 = precondition_list[p_i].find('?', index+1)
                if index1 != -1:
                    vars.append(precondition_list[p_i][index+1:index1].replace(',', '').strip())
                else:
                    vars.append(precondition_list[p_i][index+1:].replace(')', '').replace(',', '').strip())
                index = index1
            if precondition_list[p_i].startswith('!'):
                fo_ltl = fo_ltl + '(!' + precondition_list[p_i].replace('?', '')[1:] + ' S ' + 'not_' + precondition_list[p_i].replace('?', '')[1:] + ')'
            else:
                fo_ltl = fo_ltl + '(!' + 'not_' + precondition_list[p_i].replace('?', '') + ' S ' + precondition_list[p_i].replace('?', '') + ')'

            # if precondition_list[p_i][:precondition_list[p_i].find('(')] in dynamic_pred:
            #     fo_ltl = fo_ltl + ' & (!('
            #     aux = precondition_list[p_i]
            #     for v in vars:
            #         fo_ltl = fo_ltl + 'exists ' + v + '1 . '
            #         aux = aux.replace('?' + v, v + '1')
            #     fo_ltl = fo_ltl + aux + ') S ' + precondition_list[p_i].replace('?', '') + ')'
        # fo_ltl = fo_ltl + ') -> @('
        # for p_i in range(0, len(precondition_list)):
        #     if p_i != 0: fo_ltl = fo_ltl + ' & '
        #     fo_ltl = fo_ltl + precondition_list[p_i].replace('?', '')
        # fo_ltl = fo_ltl + ')) & ((@' + action + '('
        # for p_i in range(0, len(parameters_list)):
        #     if p_i != 0: fo_ltl = fo_ltl + ', '
        #     fo_ltl = fo_ltl + parameters_list[p_i].replace('?', '')
        # fo_ltl = fo_ltl + ')) -> ('
        # for p_i in range(0, len(effect_list)):
        #     if p_i != 0: fo_ltl = fo_ltl + ' & '
        #     fo_ltl = fo_ltl + effect_list[p_i].replace('?', '')
        # fo_ltl = fo_ltl + ')))'
        fo_ltl_list.append(fo_ltl)
        start = eff+1
    return fo_ltl_list

def instantiatedMonitor(domain_file_name, plan_file_name):
    domain = open(domain_file_name, 'r')
    domain_text = domain.read()
    domain.close()
    plan = open(plan_file_name)
    plan_list = []
    while True:
        line = plan.readline()
        if not line:
            break
        plan_list.append(line.replace('(', '').replace(')', '').replace('\n', '').split(' '))
    plan.close()

    start = 0
    domain_dict = {}
    # dynamic_pred = set()

    while True:
        act = domain_text.find(':action', start)
        par = domain_text.find(':parameters', start)
        pre = domain_text.find(':precondition', start)
        eff = domain_text.find(':effect', start)
        if act == -1 or par == -1 or pre == -1 or eff == -1:
            break
        next_act = domain_text.find(':action', par)
        action, parameters_list, precondition_list, effect_list = extract_info(domain_text, act, par, pre, eff, next_act)
        # for e in effect_list:
        #     if not e.startswith('!'):
        #         dynamic_pred.add(e[:e.find('(')])
        domain_dict[action] = (parameters_list, precondition_list, effect_list)
        start = eff+1

    ltl_list = []
    count = 0
    # next_effects = []
    for p in plan_list:
        p[0] = 'act_' + p[0]
        act_def = domain_dict[p[0].replace('-', '_')]
        ltl = 'H(' + p[0].replace('-', '_') + '('
        for p_i in range(1, len(p)):
            if p_i != 1: ltl = ltl + ', '
            ltl = ltl + '"' + p[p_i].replace('-', '_') + '"'
        ltl = ltl + ') -> '
        # act_def[1].extend(next_effects)
        # ground_preconditions = []
        for j in range(0, len(act_def[1])):
            if j != 0: ltl = ltl + ' & '
            aux = act_def[1][j]
            vars = []
            for i in range(1, len(p)):
                if act_def[0][i-1] in aux:
                    vars.append(act_def[0][i-1].replace('?', ''))
                aux = aux.replace(act_def[0][i-1], '"' + p[i].replace('-', '_') + '"')
            # ground_preconditions.append(aux)
            if aux.startswith('!'):
                ltl = ltl + '(!' + aux[1:] + ' S ' + 'not_' + aux[1:] + ')'
            else:
                ltl = ltl + '(!' + 'not_' + aux + ' S ' + aux + ')'
            # if aux[:aux.find('(')] in dynamic_pred:
            #     d_f = open(domain_folder + '/' + aux[:aux.find('(')].replace('_', '-') + '.json', 'r')
            #     pred_type = json.load(d_f)
            #     d_f.close()
            #     perm = []
            #     n = 1
            #     for i in pred_type:
            #         perm.append([0,len(pred_type[i])])
            #         n = n * len(pred_type[i])
            #     ltl = ltl + ' & (('
            #     for i in range(0, n):
            #         if i != 0:
            #             if aux.startswith('!'):
            #                 ltl = ltl + ' | '
            #             else:
            #                 ltl = ltl + ' & '
            #         incr = True
            #         first = True
            #         if aux.startswith('!'):
            #             ltl = ltl + aux[1:aux.find('(')] + '('
            #         else:
            #             ltl = ltl + '!' + aux[:aux.find('(')] + '('
            #         pr_c = 0
            #         for pr in pred_type:
            #             if first:
            #                 first = False
            #             else:
            #                 ltl = ltl + ', '
            #             ltl = ltl + '"' + pred_type[pr][perm[pr_c][0]] + '"'
            #             if incr:
            #                 perm[pr_c][0] = perm[pr_c][0] + 1
            #             if perm[pr_c][0] == perm[pr_c][1]:
            #                 perm[pr_c][0] = 0
            #                 incr = True
            #             else:
            #                 incr = False
            #             pr_c = pr_c + 1
            #         ltl = ltl + ')'
            #     ltl = ltl + ') S ' + aux + ')'
        # for j in range(0, len(ground_preconditions)):
        #     ltl = ltl + ' & ('
        #     ltl = ltl + '(' + ' | '.join(ground_preconditions) + ')'
        #     ltl = ltl + ' S ' + ground_preconditions[j] + ')'
        ltl = ltl + ')'
        ltl_list.append(ltl)
        count = count + 1
    return ltl_list
            # if next_effects:
            # ltl = ltl + '& (!('
            # for v in vars:
            #     ltl = ltl + 'exists ' + v + ' . '
            # ltl = ltl + act_def[1][j].replace('?', '') + ') S ' + aux + '))'
            # else:
                # ltl = ltl + ')'
        # next_effects = []
        # for j in range(0, len(act_def[2])):
        #     aux = act_def[2][j]
        #     for i in range(1, len(p)):
        #         aux = aux.replace(act_def[0][i-1], '"' + p[i].replace('-', '_') + '"')
        #     next_effects.append(aux)
        #
        # ltl = ltl + ') & (@(' + p[0].replace('-', '_') + '('
        # for p_i in range(1, len(p)):
        #     if p_i != 1: ltl = ltl + ', '
        #     ltl = ltl + '"' + p[p_i].replace('-', '_') + '"'
        # ltl = ltl + ')) -> ('
        # for j in range(0, len(act_def[2])):
        #     if j != 0: ltl = ltl + ' & '
        #     aux = act_def[2][j]
        #     for i in range(1, len(p)):
        #         aux = aux.replace(act_def[0][i-1], '"' + p[i].replace('-', '_') + '"')
        #     ltl = ltl + aux
        # ltl = ltl + '))))'


def extract_info(domain_text, act, par, pre, eff, next_act):
    action = 'act_' + domain_text[act+7:par].replace('\n', '').replace('-', '_').strip()
    parameters = domain_text[par+11:pre].replace('\n', '').strip()
    precondition = domain_text[pre+13:eff].replace('\n', '').replace('and', '').strip()
    if next_act != -1:
        effect = domain_text[eff+7:next_act-1].replace('\n', '').replace('and', '').strip()
    else:
        effect = domain_text[eff+7:-1].replace('\n', '').replace('and', '').strip()

    p_start = 0
    parameters_list = []
    while parameters.find('?', p_start) != -1:
        i = parameters.find('?', p_start)
        j = parameters.find('-', p_start)
        if j != -1:
            parameters_list.append(parameters[i:j].replace('-', '_').strip())
        else:
            parameters_list.append(parameters[i:len(parameters)-1].replace('-', '_').strip())
        p_start = j+1

    p_start = 0
    precondition_list = []
    while precondition.find(')', p_start) != -1:
        i = precondition.find(')', p_start)
        if i != -1:
            aux = precondition[p_start:i].replace('(', '').replace(')', '').strip()
        else:
            aux = parameters[p_start:len(parameters)-1].replace('(', '').replace(')', '').strip()
        if aux:
            if aux.startswith('not'):
                ii = aux.find(' ')
                aux = '!' + aux[ii+1:aux.find(' ', ii+1)] + '(' + aux[aux.find(' ', ii+1)+1:].replace(' ', ', ') + ')'
            else:
                aux = aux[0:aux.find(' ')] + '(' + aux[aux.find(' ')+1:].replace(' ', ', ') + ')'
            precondition_list.append(aux.replace('-', '_'))
        p_start = i+1
    p_start = 0
    effect_list = []
    while effect.find(')', p_start) != -1:
        i = effect.find(')', p_start)
        if i != -1:
            aux = effect[p_start:i].replace('(', '').replace(')', '').strip()
        else:
            aux = effect[p_start:len(parameters)-1].replace('(', '').replace(')', '').strip()
        if aux:
            if aux.startswith('not'):
                ii = aux.find(' ')
                aux = '!' + aux[ii+1:aux.find(' ', ii+1)] + '(' + aux[aux.find(' ', ii+1)+1:].replace(' ', ', ') + ')'
            else:
                aux = aux[0:aux.find(' ')] + '(' + aux[aux.find(' ')+1:].replace(' ', ', ') + ')'
            effect_list.append(aux.replace('-', '_'))
        p_start = i+1
    return action, parameters_list, precondition_list, effect_list

def main(args):
    start_time = time.time()
    if len(args) == 2:
        fo_ltl_list = parameterisedMonitor(args[1])
        for fo_ltl in fo_ltl_list:
            print(fo_ltl)
        f = open('./out/prop.qtl', 'w')
        i = 0
        for fo_ltl in fo_ltl_list:
            f.write('prop fo_ltl_' + str(i) + ' :\n')
            f.write('\t' + fo_ltl + '\n\n')
            i = i + 1
        f.close()
        prop_time = (time.time() - start_time)
        print("#Property generation# --- %s seconds ---" % (time.time() - start_time))
        mon_time = start()
        return prop_time, mon_time
    elif len(args) == 3:
        ltl_list = instantiatedMonitor(args[1], args[2])
        for ltl in ltl_list:
            print(ltl)
        f = open('./out/prop.qtl', 'w')
        i = 0
        for ltl in ltl_list:
            f.write('prop ltl_' + str(i) + ' :\n')
            f.write('\t' + ltl + '\n\n')
            i = i + 1
        f.close()
        prop_time = (time.time() - start_time)
        print("#Property generation# --- %s seconds ---" % (time.time() - start_time))
        mon_time = start()
        return prop_time, mon_time
        # os.system('scalac -cp .:./dejavu_akka.jar TraceMonitor.scala 2>&1')
    else:
        print('usage: <domain_file_name> <plan_file_name> (<plan_file_name> is required only for the instantiated version)')
def start():
    start_time = time.time()
    os.system('java -cp ./online/dejavu.jar dejavu.Verify ./out/prop.qtl')
    mon_time = (time.time() - start_time)
    print("#Monitor generation# --- %s seconds ---" % (time.time() - start_time))
    # os.system('cp ./TraceMonitor.scala ./online/src/main/scala/')
    # os.system('cp ./TraceMonitor.scala ../dejavu/')
    return mon_time
if __name__ == '__main__':
    main(sys.argv)






# LTL
# for p in plan_list:
#     act_def = domain_dict[p[0]]
#     ltl = ''
#     for i in range(0, count):
#         ltl = 'X(' + ltl
#     for j in range(0, len(act_def[1])):
#         if j != 0: ltl = ltl + ' & '
#         aux = act_def[1][j]
#         for i in range(1, len(p)):
#             aux = aux.replace(act_def[0][i-1], p[i])
#         ltl = ltl + aux
#     ltl = ltl + ' & X('
#     for j in range(0, len(act_def[2])):
#         if j != 0: ltl = ltl + ' & '
#         aux = act_def[2][j]
#         for i in range(1, len(p)):
#             aux = aux.replace(act_def[0][i-1], p[i])
#         ltl = ltl + aux
#     ltl = ltl + ')'
#     for i in range(0, count):
#         ltl = ltl + ')'
#     ltl_list.append(ltl)
#     count = count + 1
