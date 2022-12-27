d = {}
for k,v in [e.strip().split(": ") for e in open("input.txt","rt")]:
  d[k] = v.split()

def calc(n):
  w = d[n]
  if len(w)==1: return int(w[0])
  w1,w2 = calc(w[0]),calc(w[2])
  match w[1]:
    case'+': return w1+w2
    case'-': return w1-w2
    case'*': return w1*w2
    case'/': return w1//w2

def mark(n,h):
  w = d[n]
  if len(w)==1: return n==h
  if mark(w[0],h): d[n].append(1); return True # to solve left
  if mark(w[2],h): d[n].append(0); return True # to solve right
  return False # just calculate

def solve(n,a):
  w = d[n]
  if len(w)==1: return a
  if w[3]: # solve left
    k = calc(w[2])
    match w[1]:
      case'+': return solve(w[0],a-k) # reverse ops for left
      case'*': return solve(w[0],a//k)
      case'-': return solve(w[0],a+k)
      case'/': return solve(w[0],a*k)
  else: # solve right
    k = calc(w[0])
    match w[1]:
      case'+': return solve(w[2],a-k) # reverse ops for right
      case'*': return solve(w[2],a//k)
      case'-': return solve(w[2],k-a)
      case'/': return solve(w[2],k//a)

def solve_top(n,h):
  mark(n,h)
  w = d[n]
  if w[3]:return solve(w[0],calc(w[2])) # solve left
  else: return solve(w[2],calc(w[0])) # solve right

print( calc('root'), solve_top('root','humn') )