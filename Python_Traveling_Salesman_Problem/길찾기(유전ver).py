# -*- coding: utf-8 -*-
"""길찾기(유전ver).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lYZHxOwXALKc2i2dh1QD7h2Yk6zwGo1J
"""

#과제_최종
import random
import math
import copy
import time
from turtle import *

t = time.time()

city_n = 20          #도시 개수
population_n = 100   #20개의 도시를 연결해주는 경로의 경우의 수 중 100개만 생각하겠다=개체집단의 크기
population = []      #유전자 모음[[][][][]...[]]
generation_n = 100   #100세대까지만 계산하겠다
mutation_rate = 0.2  #돌연변이 확률
city = []
start_city = [] # start = destination

class Chromosome:
  def __init__(self,g=[]):
    global start_city
    global city
    self.genes = g.copy()
    self.fitness = 0
    if self.genes.__len__()==0:
      self.path = random.sample(city[1:], len(city)-1)
      self.genes = [start_city] + self.path + [start_city]


  def cal_fitness(self): #적합도를 계산해주는 함수
    i = 0
    total_distance = 0
    distance = []
    for i in range(20):
      x = abs(self.genes[i][0] - self.genes[i+1][0])**2 #x
      y = abs(self.genes[i][1] - self.genes[i+1][1])**2 #y
      distance.append(math.sqrt(x+y));
    total_distance = sum(distance) #도착지까지 총 걸리는 거리를 비교
    self.fitness = 1/total_distance*10000 
    #적합도는 높을수록 좋지만 거리값은 낮을수록 좋기때문에 역수를 취해줌
    return self.fitness
    
def print_p(pop):
  i = 0
  for x in pop:
    print("염색체 #", i, '=', x, "적합도 = ", x.cal_fitness())
    i += 1
  print("")

#돌연변이 연산 : 한부모라서 random으로 둘의 위치를 바꿔줌
def mutate(c):
  #print(c.genes)
  for i in range(city_n):
    if random.random() < mutation_rate:
      temp = 0
      change_index1 = random.randint(1,19) #a,b 도 포함 시작지와 도착지는 예외
      change_index2 = random.randint(1,19)
      temp = c.genes[change_index1]
      c.genes[change_index1] = c.genes[change_index2]
      c.genes[change_index2] = temp


# 유전자 crossover
def crossover(best1):
  parent = copy.deepcopy(best1)
  change_index1 = random.randint(2,19)
  change_index2 = random.randint(2,19)
  temp = 0

  temp = parent[change_index1]
  parent[change_index1] = parent[change_index2]
  parent[change_index2] = temp
  child = parent

  return (child)

def draw_map(path):
  penup()
  goto(path[0])
  pendown()
  for i in range(1, 21):
    x = path[i][0]
    y = path[i][1]
    goto(x, y)
  mainloop()


########################  main문  #############################
count = 0
while count<city_n:
  x = random.randint(0,100)
  y = random.randint(0,100)
  new_city = [x,y]
  if new_city in city:
    pass
  else:
    city.append(new_city)
    count = count+1
print("city = ",city)
start_city = city[0]

#초기 염색체를 생성하여 객체 집단에 추가
i = 0
while i<population_n:
  population.append(Chromosome())
  i+=1


count = 0
population.sort(key=lambda x: x.cal_fitness(), reverse=True)
count += 1

while population[0].fitness<50:
  population.sort(key=lambda x: x.cal_fitness(), reverse=True)
# 부모의 수를 하나로 한다
  new_pop = []
  #print("old_적합도",population[0].fitness)
  b = population[0].genes
  #print("old_best=",b)
  #new_pop.append(population[0])
  for k in range(0,51):  #n개
    new = crossover(b) #new = list
    new_pop.append(Chromosome(new))
    #print(new_pop[k].fitness) == 0
  for j in range(0,24): #50-n개는 새로 생성
    new_pop.append(Chromosome())
  for c in new_pop: mutate(c)
  new_pop.append(Chromosome(population[0].genes))

  
  population = copy.deepcopy(new_pop) #new_pop.copy()
  #print(population[-1].genes == b) #list==list
  #print("적합도",population[3].fitness)

  population.sort(key=lambda x: x.cal_fitness(), reverse=True)
  count += 1

  if count > 1500 : break #적정 횟수 이상 넘어가면 반복문 중단하고 끝내기

print("path = ",population[0].genes) #list==list
print("적합도 = ",population[0].fitness)
print("time = ", time.time() - t)  # 현재시각 - 시작시간 = 실행 시간
draw_map(population[0].genes)