import random
guess = ''
while guess not in ('heads','tails'):
     print('Guess the coin toss! Enter heads or tails:')
     guess = input().lower()
     if guess not in ('heads','tails'):
          print ('请重新输入heads或tails:')
toss = random.randint(0,1)#0 is tails,1 is heads
if toss ==0:
     toss = 'heads'
else:toss = 'tails'
if toss ==guess:
     print('You got it!')
else:
     print('Nope!Guess again!')
     guess = input().lower()
     if toss == guess:
          print('You got it！')
     else:
          print('Nope.You are really.bad at this game.')
          
