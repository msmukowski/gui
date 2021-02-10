from helpers import Target


obj = Target()

while obj.run:
    obj.update()

    if obj.key_cap == ord('q'):
        obj.cleanup()
    else:
        obj.display(obj.result)

