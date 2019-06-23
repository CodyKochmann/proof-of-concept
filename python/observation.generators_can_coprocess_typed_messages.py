 #!/usr/bin/env python3
 # by: Cody Kochmann

from itertools import cycle

''' this demonstrates how a python generator can be 
sent actor style messages via exceptions to delegate 
what logic gets applied to each message by taking 
advantage of the easy to use mapping try/except trees
already provide '''


class NewRRActor(BaseException):
    ''' Specifies actors that will be added to a round robin cycler '''
    
class ExpiredRRActor(BaseException):
    ''' Specifies actors that have expired and should be removed from a round robin schedule '''

def round_robin(*actors):
    ''' this acts as a round robin scheduler for multiple iterators '''
    
    # verifies that all actors are iterable
    actors = [a for a in actors if iter(a)]
    
    while True:
        try:
            ''' This "try" block is essentially this
            actor's main processing "tick". If an 
            exception is thrown, the main tick pauses 
            for a moment and handles the exception. 
            Normal processing resumes on the next
            "tick". '''
            for next_actor in cycle(actors):
                for next_message in next_actor:
                    yield next_message
                    break
                
        except NewRRActor as message:
            # logic to add new actors
            for new_actor in message.args:
                actors.append(new_actor)
            yield  # end of "tick"
            
        except ExpiredRRActor as message:
            # logic to remove expired actors
            for expired_actor in message.args:
                while expired_actor in actors:
                    actors.remove(expired_actor)
            yield  # end of tick
            
            
def test_actor(*, name, counts_to):
    ''' this is just a test iterator that infinitely 
    yields the name and the next number in the 
    sequence to demonstrate individual processing and
    private state within each individual actor '''
    
    for i in cycle(range(counts_to)):
        yield name, i
        

if __name__ == '__main__':
    
    rr = round_robin(
        test_actor(
            name='marcin',
            counts_to=10
        ),
        test_actor(
            name='daniel',
            counts_to=3
        )
    )
    
    new_guy = test_actor(
        name='cody',
        counts_to=4
    )
    
    ''' the loop below iterates over the first 30 
    messages out of the round robin pipeline while
    demonstrating how you can use typed message 
    passing to modify the pipeline without needing to 
    restart the iteration process '''
    
    for i,message in zip(range(30), rr):
        print(message)
        if i is 10:
            print('adding cody')
            rr.throw(NewRRActor(new_guy))
        elif i is 20:
            print('expiring cody')
            rr.throw(ExpiredRRActor(new_guy))
