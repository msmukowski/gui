from helpers import Target


def main():
    obj = Target()

    while obj.run:
        obj.update()

        if obj.key_cap == ord('q'):
            obj.cleanup()
        else:
            obj.display(obj.result)


if __name__ == '__main__':
    main()
