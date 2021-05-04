import translator
import generate_plan
import sys
import time
import os

def main(args):
    f = open('res.csv', 'w')
    f.close()
    for n in range(int(args[1]), int(args[2]), int(args[3])):
        with open('res.csv', 'a') as f:
            generate_plan.main([None, n])
            # prop_time, mon_time = translator.main([None, 'domain.pddl', 'new_plan.txt', 'domain'])
            # f.write(str(n) + ',' + str(prop_time) + ',' + str(mon_time))
            start_time = time.time()
            os.system('../dejavu/dejavu new_plan.csv')
            f.write(str(n) + ',' + str(time.time() - start_time) + '\n')
if __name__ == '__main__':
    main(sys.argv)
