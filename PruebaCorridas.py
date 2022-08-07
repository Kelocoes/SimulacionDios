import math 


def runsTest(l, l_median): 

    runs, n1, n2 = 0, 0, 0
    
    for i in range(len(l)): 

        if (l[i] >= l_median and l[i-1] < l_median) or (l[i] < l_median and l[i-1] >= l_median): 
            runs += 1  

        
        if(l[i]) >= l_median: 
            n1 += 1   

        
        else: 
            n2 += 1   

    miu = ((2*n1*n2)/(n1+n2))+1
    desvesta = math.sqrt((2*n1*n2*(2*n1*n2-n1-n2))/(((n1+n2)**2)*(n1+n2-1))) 

    print(runs)

    if (-1.96*desvesta + miu <= runs and runs <= 1.96*desvesta + miu):
        print("Es independiente")
    else:
        print("No es independiente")

