import sys

def main(args):
    length = int(args[1])
    f = open('./new_plan.txt', 'w')
    csv = open('./new_plan.csv', 'w')
    for i in range(0, length):
        cell0 = 'cell_0_' + str(i)
        cell1 = 'cell_1_' + str(i)
        cell2 = 'cell_2_' + str(i)
        cell3 = 'cell_1_' + str(i + 1)
        cell4 = 'cell_1_' + str(i + 2)
        cell5 = 'cell_2_' + str(i + 2)
        f.write('''(right rover {c0} {c1})
(inspect-right rover {c1} {c2} tank1)
(down rover {c1} {c3})
(down rover {c3} {c4})
(inspect-right rover {c4} {c5} tank2)
'''.format(c0=cell0, c1=cell1, c2=cell2, c3=cell3, c4=cell4, c5=cell5))
        csv.write('''not_radiation,{c0}
not_radiation,{c1}
not_radiation,{c2}
not_radiation,{c3}
not_radiation,{c4}
not_radiation,{c5}
not_inspected,tank1
not_inspected,tank2
robot_at,rover,{c0}
right,{c0},{c1}
empty,{c1}
not_empty,{c0}
act_right,rover,{c0},{c1}
not_robot_at,rover,{c0}
not_empty,{c1}
robot_at,rover,{c1}
empty,{c0}
tank_at,tank1,{c2}
right,{c1},{c2}
act_inspect_right,rover,{c1},{c2},tank1
inspected,tank1
down,{c1},{c3}
empty,{c3}
act_down,rover,{c1},{c3}
robot_at,rover,{c3}
not_robot_at,rover,{c1}
not_empty,{c3}
empty,{c1}
down,{c3},{c4}
empty,{c4}
act_down,rover,{c3},{c4}
robot_at,rover,{c4}
not_robot_at,rover,{c3}
empty,{c3}
not_empty,{c4}
tank_at,tank2,{c5}
right,{c4},{c5}
act_inspect_right,rover,{c4},{c5},tank2
inspected,tank2
'''.format(c0=cell0, c1=cell1, c2=cell2, c3=cell3, c4=cell4, c5=cell5))
    f.close()
if __name__ == '__main__':
    main(sys.argv)
