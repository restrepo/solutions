import numpy as np
import pandas as pd
import itertools
import random
import itertools
from itertools import permutations

def get_hidden_sector(l): #generar todas las parejas posibles dada una lista del DF('solution) #IDEA longitud de las listas se igual a lo que sumen las parejas
   parejas=[]
   com=list(itertools.combinations(l,2))
   Dd=list((i,i) for i in l)
   L=com+Dd
   par=int(len(l)/2)
   impar=int((len(l)+1)/2)
  
   if not l:
     return []
   if len(l) %2 != 0:

      flatten_2=list(itertools.combinations(L,impar))

     

      for item in flatten_2:
        for x in item:
          conv=list(map(list, item))
          sol=[abs(sum(p)) for p in conv] 
         
      

          
      if sol.count(sol[0])!=len(sol):
        flatten=[item for sublist in  conv for item in sublist]
        dif=[element for element in l if element not in flatten]# coloca los numeros que estan en l pero no en flatten
        

        if  dif :
          count1=[i for i in l if l.count(i)==2] #elementos de l1  DOS VECES ;[{}; ([2,-3,-4,5,-6,7,7,-8],[[2,-3],[-4,5],[-6,7],[7,-8]])
          count2=[j for j in conv if conv.count(j)==1]  #elementos de m repetidos, donde m son la lista de tuplas que ingresan a get_pairs#  
          if len(count1)==0:
            if len(count2)==4: 
              if sol[0]!=4:
                return []   
            else:
                  parejas.append({'S':sol[0],'ψ':conv})# salida test: 1
          if len(count1)==2:
            if len(count2)==4:
              return []
          if len(count1)==4:
            if len(count2)==2:
              return []

   else:

      flatten_2=list(itertools.combinations(L,par))
     
      for item in flatten_2:
        for x in item:
          conv=list(map(list, item))
          sol=[abs(sum(p)) for p in conv]
          #print(sol)
        if sol.count(sol[0])==len(sol):

        
          flatten=[item for sublist in  conv for item in sublist]
          dif=[element for element in l if element not in flatten]# coloca los numeros que estan en l pero no en flatten
          #
          if not dif :
            
            
            count1=[i for i in l if l.count(i)==2] #elementos de l1  DOS VECES ;[{}; ([2,-3,-4,5,-6,7,7,-8],[[2,-3],[-4,5],[-6,7],[7,-8]])
            count2=[j for j in conv if conv.count(j)==1]  #elementos de m repetidos, donde m son la lista de tuplas que ingresan a get_pairs#
            if len(count1)==2:
              if len(count2)==4:
                   parejas.append({'S':sol[0],'ψ':conv})
                  
              if len(count2)==3:
                l_organizada=sorted(l)
                flatten_organizada=sorted(flatten)
                diferencia = [e1 - e2 for e1, e2 in zip(l_organizada,flatten_organizada)]
                resultado = [x for x in diferencia if x!=0] 
                if len(resultado)==0:
                 parejas.append({'S':sol[0],'ψ':conv})
                else:
                   return []      
            if len(count1)==6:
                 parejas.append({'S':sol[0],'ψ':conv})

            if len(count1)==2:   
                if len(count2)==2:
                  parejas.append({'S':sol[0],'ψ':conv})
                if len(count2)==6:
                  parejas.append({'S':sol[0],'ψ':conv})
                if len(count2)==3:
                  parejas.append({'S':sol[0],'ψ':conv})  

            if len(count1)==0:
               
                if len(count2)==0:
                  return [] 
                if len(count2)==4:
                  parejas.append({'S':sol[0],'ψ':conv}) #cambio daño test 7
                if len(count2)<3:
                    parejas.append({'S':sol[0],'ψ':conv}) 
                if len(count2)==10: 
                  return []

            if len(count1)==4: 
                if len(count2)==4:
                  parejas.append({'S':sol[0],'ψ':conv}) 

            if len(count2)==2:
                if len(count2)==6:
                  parejas.append({'S':sol[0],'ψ':conv})      
          
   return parejas



assert get_hidden_sector([1,2,-3,4,5])[0].get('S')==6
assert get_hidden_sector([1,2,-3,-3,4,5])[0].get('S')==6
assert get_hidden_sector([1,1,2,-3,-3,4,5,5])[0].get('S')==6
#aψ1ψ1+bψ1ψ2+cψ1,ψ3 → https://www.wolframalpha.com/input?i=Rank%20{{a,b,c},{b,0,0},{c,0,0}}
assert get_hidden_sector([1,2,-3,4,5,9,9])==[]
get_hidden_sector([1,1,2,-3,4,5])
#aψ1ψ2+bψ1ψ3 → https://www.wolframalpha.com/input?i=rank+{{0,a,b},{a,0,0},{b,0,0}}
assert get_hidden_sector([1,1,2,-3,4,5])==[]
assert get_hidden_sector([1,1,2,-3,-3,4,5])==[]
assert get_hidden_sector([1,2,-3,4,5,8])==[]
assert get_hidden_sector([1,2,-3,4,5,8,8])==[]
assert get_hidden_sector([])==[]
assert get_hidden_sector([1, 1, 1, 1, 1, -2, -2, -2, -2, 3])==[]
assert get_hidden_sector([1, 2, 2, 2, -3, -5, -6, 7])[0].get('S')==4
assert get_hidden_sector( [1, 2, 2, 4, -5, -5, -7, 8] )[0].get('S')==3
# Ana test
assert get_hidden_sector([2, -3, -4, 5, -6, 7, 7, -8])[0].get('S')==1
assert get_hidden_sector([3, 5, -8, 9, -10, -14, 15])==[] # Dirac triplet [-10,5,15] (s=5)
assert get_hidden_sector([3, 5, -8, 9, -10, -14, 15, 20,-30, 35])==[] 
